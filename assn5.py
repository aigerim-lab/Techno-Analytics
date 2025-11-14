import sys
from pathlib import Path

import numpy as np
import open3d as o3d
import trimesh

# ================== CONFIG ==================

POINTS_FOR_SAMPLING = 15000
PLANE_NORMAL = np.array([1.0, 0.0, 0.0])
PLANE_OFFSET = 0.0  # плоскость x = 0

# ================== HELPERS ==================

def center_geometry(geom):
    """Центрирует геометрию в (0,0,0)."""
    bb = geom.get_axis_aligned_bounding_box()
    center = bb.get_center()
    geom.translate(-center)
    return geom


def print_mesh_info(title, mesh: o3d.geometry.TriangleMesh):
    print(f"\n=== {title} ===")
    print(f"Vertices: {len(mesh.vertices)}")
    print(f"Triangles: {len(mesh.triangles)}")
    print(f"Has colors: {mesh.has_vertex_colors()}")
    print(f"Has normals: {mesh.has_vertex_normals()}")


def print_pcd_info(title, pcd: o3d.geometry.PointCloud):
    print(f"\n=== {title} ===")
    print(f"Points: {len(pcd.points)}")
    print(f"Has colors: {pcd.has_colors()}")
    print(f"Has normals: {pcd.has_normals()}")


def load_and_triangulate(model_path: Path) -> Path:
    """Загружает модель через trimesh, триангулирует и сохраняет во временный *_tri.obj."""
    print(f"🔹 Loading model: {model_path}")
    mesh = trimesh.load(model_path, force="mesh")

    if hasattr(mesh, "triangulate"):
        mesh = mesh.triangulate()
        print("✅ Triangulated successfully.")
    else:
        print("⚠️ Triangulation not available.")

    # лёгкая чистка
    mesh.remove_infinite_values()
    mesh.remove_duplicate_faces()
    mesh.remove_degenerate_faces()

    out_path = model_path.with_name(model_path.stem + "_tri.obj")
    mesh.export(out_path)
    print(f"✅ Saved cleaned mesh → {out_path.name}")
    return out_path


def make_sphere(center, radius=0.05, color=(1.0, 0.0, 0.0)):
    s = o3d.geometry.TriangleMesh.create_sphere(radius=radius)
    s.translate(center)
    s.paint_uniform_color(color)
    s.compute_vertex_normals()
    return s


def make_arrow_at(center, length=0.25, color=(1.0, 0.0, 0.0)):
    """Небольшая стрелка вдоль +Z в указанной точке."""
    cyl_r, cone_r = length * 0.05, length * 0.09
    cyl_h, cone_h = length * 0.7, length * 0.3
    arr = o3d.geometry.TriangleMesh.create_arrow(
        cylinder_radius=cyl_r,
        cone_radius=cone_r,
        cylinder_height=cyl_h,
        cone_height=cone_h,
    )
    arr.paint_uniform_color(color)
    arr.translate(center)
    arr.compute_vertex_normals()
    return arr


# -------- Colorful voxel helpers (для Step 4) --------

def _colormap01(t: np.ndarray) -> np.ndarray:
    """Простой градиент R→Y→G→C→B для значений 0..1."""
    t = np.clip(t, 0.0, 1.0)
    c = np.zeros((t.size, 3), float)
    seg = np.minimum(4, (t * 4).astype(int))
    w = (t * 4) - seg

    # R(1,0,0)->Y(1,1,0)
    m = seg == 0
    c[m] = np.stack([np.ones(m.sum()), w[m], np.zeros(m.sum())], 1)
    # Y(1,1,0)->G(0,1,0)
    m = seg == 1
    c[m] = np.stack([1.0 - w[m], np.ones(m.sum()), np.zeros(m.sum())], 1)
    # G(0,1,0)->C(0,1,1)
    m = seg == 2
    c[m] = np.stack([np.zeros(m.sum()), np.ones(m.sum()), w[m]], 1)
    # C(0,1,1)->B(0,0,1)
    m = seg >= 3
    c[m] = np.stack([np.zeros(m.sum()), 1.0 - w[m], np.ones(m.sum())], 1)
    return c


def build_colored_voxel_mesh_from_pcd(pcd: o3d.geometry.PointCloud) -> tuple[o3d.geometry.TriangleMesh, float, int]:
    """
    Делает «LEGO»-представление: кубик на каждый занятый воксель.
    Цвет кубика — по средней высоте Z в этом вокселе.
    Возвращает (меш, voxel_size, num_voxels).
    """
    pts = np.asarray(pcd.points)
    if pts.size == 0:
        raise RuntimeError("Point cloud is empty for voxelization")

    # подберём размер вокселя ≈ 30 кубиков по максимальному измерению
    bb = pcd.get_axis_aligned_bounding_box()
    diag = bb.get_max_bound() - bb.get_min_bound()
    max_dim = float(diag.max())
    voxel_size = max_dim / 30.0  # можно поменять на 20.0 для более крупных кубиков

    origin = pts.min(axis=0)
    ijk = np.floor((pts - origin) / voxel_size).astype(np.int32)

    keys, inv = np.unique(ijk, axis=0, return_inverse=True)
    num_vox = len(keys)

    # средний Z по каждому вокселю
    z_mean = np.zeros(num_vox, float)
    for k in range(num_vox):
        z_mean[k] = pts[inv == k, 2].mean()

    # нормируем Z для цвета
    z0, z1 = z_mean.min(), z_mean.max()
    z_norm = (z_mean - z0) / (z1 - z0 + 1e-12)
    colors = _colormap01(z_norm)

    # базовый куб (единичный)
    base_box = o3d.geometry.TriangleMesh.create_box(1.0, 1.0, 1.0)
    vb = np.asarray(base_box.vertices)
    tb = np.asarray(base_box.triangles)

    all_v = []
    all_f = []
    all_c = []

    for idx, (cell, col) in enumerate(zip(keys, colors)):
        center = origin + (cell + 0.5) * voxel_size
        verts = vb * voxel_size + (center - 0.5 * voxel_size)

        all_v.append(verts)
        all_f.append(tb + idx * len(vb))
        all_c.append(np.tile(col, (len(vb), 1)))

    V = np.vstack(all_v)
    F = np.vstack(all_f)
    C = np.vstack(all_c)

    vox_mesh = o3d.geometry.TriangleMesh(
        o3d.utility.Vector3dVector(V),
        o3d.utility.Vector3iVector(F),
    )
    vox_mesh.vertex_colors = o3d.utility.Vector3dVector(C)
    vox_mesh.compute_vertex_normals()
    return vox_mesh, voxel_size, num_vox


# ================== MAIN PIPELINE ==================

def main():
    if len(sys.argv) < 2:
        print("Usage: python ass5.py <path/to/12219_boat_v2_L2.obj>")
        sys.exit(1)

    model_path = Path(sys.argv[1])
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")

    # ---- Step 1: загрузка + триангуляция ----
    tri_path = load_and_triangulate(model_path)
    mesh = o3d.io.read_triangle_mesh(str(tri_path))
    if mesh.is_empty():
        raise RuntimeError("Failed to load mesh")
    mesh.compute_vertex_normals()
    mesh = center_geometry(mesh)
    print_mesh_info("Step 1 : Original Mesh", mesh)
    o3d.visualization.draw_geometries([mesh], window_name="Step 1 – Original Model")

    # ---- Step 2: Point Cloud ----
    pcd = mesh.sample_points_poisson_disk(POINTS_FOR_SAMPLING)
    print_pcd_info("Step 2 : Point Cloud (from mesh)", pcd)
    o3d.visualization.draw_geometries([pcd], window_name="Step 2 – Point Cloud")

    # ---- Step 3: Surface Reconstruction (Poisson) ----
    print("\n=== Step 3 : Surface Reconstruction (Poisson) ===")
    pcd.estimate_normals()
    mesh_rec, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=6
    )
    densities = np.asarray(densities)
    thr = np.quantile(densities, 0.3)
    mesh_rec = mesh_rec.select_by_index(np.where(densities > thr)[0])
    mesh_rec.compute_vertex_normals()
    mesh_rec = center_geometry(mesh_rec)
    print_mesh_info("Step 3 : Reconstructed Mesh", mesh_rec)
    o3d.visualization.draw_geometries(
        [mesh_rec], window_name="Step 3 – Reconstructed Surface"
    )

    # ---- Step 4: Colorful Voxelization (исправленный) ----
    vox_mesh, voxel_size, num_vox = build_colored_voxel_mesh_from_pcd(pcd)
    print(f"\n=== Step 4 : Colorful Voxelization ===")
    print(f"Voxel size = {voxel_size:.3f}, Voxels (cubes) = {num_vox}")
    print("Presence of color: True (vertex_colors on voxel mesh)")
    o3d.visualization.draw_geometries(
        [vox_mesh], window_name="Step 4 – Colorful Voxel Grid"
    )

    # ---- Step 5: Plane ----
    plane_size = 1.2 * np.max(mesh.get_max_bound() - mesh.get_min_bound())
    half = plane_size / 2
    plane_vertices = np.array(
        [
            [PLANE_OFFSET, -half, -half],
            [PLANE_OFFSET, -half, half],
            [PLANE_OFFSET, half, half],
            [PLANE_OFFSET, half, -half],
        ]
    )
    plane_triangles = np.array([[0, 1, 2], [0, 2, 3]])
    plane = o3d.geometry.TriangleMesh(
        o3d.utility.Vector3dVector(plane_vertices),
        o3d.utility.Vector3iVector(plane_triangles),
    )
    plane.paint_uniform_color([0.8, 0.8, 0.2])
    plane.compute_vertex_normals()
    o3d.visualization.draw_geometries(
        [mesh_rec, plane], window_name="Step 5 – Plane Added"
    )

    # ---- Step 6: Clipping ----
    p0 = np.array([PLANE_OFFSET, 0.0, 0.0])
    n = PLANE_NORMAL / np.linalg.norm(PLANE_NORMAL)
    pts = np.asarray(pcd.points)
    side = (pts - p0) @ n
    keep_idx = np.where(side <= 0)[0]
    pcd_clipped = pcd.select_by_index(keep_idx)
    print_pcd_info("Step 6 : Clipped Point Cloud", pcd_clipped)
    o3d.visualization.draw_geometries(
        [pcd_clipped, plane], window_name="Step 6 – After Clipping"
    )

        # ---- Step 7: Gradient + visible min/max (IMPROVED) ----
    # ---- Step 7: Gradient + visible min/max (IMPROVED) ----
    # ---- Step 7: Gradient + Visible Min/Max (CUBE MARKERS) ----
    # ---- Step 7: Gradient + LARGE Visible Min/Max ----
    pts = np.asarray(pcd_clipped.points)
    if pts.size == 0:
        raise RuntimeError("No points after clipping — adjust PLANE_OFFSET.")

    z = pts[:, 2]
    z_min, z_max = float(z.min()), float(z.max())
    z_norm = (z - z_min) / (z_max - z_min + 1e-12)

# Color gradient
    colors = np.vstack([z_norm, 0.3*np.ones_like(z_norm), 1.0 - z_norm]).T
    pcd_clipped.colors = o3d.utility.Vector3dVector(colors)

    imin, imax = int(np.argmin(z)), int(np.argmax(z))
    p_min, p_max = pts[imin], pts[imax]

    print("\n=== Step 7 : Color & Extremes ===")
    print(f"Z min = {z_min:.4f}  at {p_min}")
    print(f"Z max = {z_max:.4f}  at {p_max}")

# A) VERY LARGE cubes (always visible)
    def big_cube(center, size=50, color=(1,0,0)):
        c = o3d.geometry.TriangleMesh.create_box(size, size, size)
        c.translate(center - np.array([size/2, size/2, size/2]))
        c.paint_uniform_color(color)
        c.compute_vertex_normals()
        return c

    cube_min = big_cube(p_min, size=80, color=(1,0,0))   # huge red cube
    cube_max = big_cube(p_max, size=80, color=(0,1,0))   # huge green cube

# B) Giant text-panels
    def text_panel(center, text="MIN"):
        w, h = 120, 40
        panel = o3d.geometry.TriangleMesh.create_box(w, h, 2)
        panel.translate(center + np.array([100, 0, 0]))   # shift to the side
        panel.paint_uniform_color([0.9, 0.9, 0.9])
        panel.compute_vertex_normals()
        return panel

    panel_min = text_panel(p_min, "MIN")
    panel_max = text_panel(p_max, "MAX")

# C) Up/Down arrows
    def arrow(center, direction=np.array([0,0,1]), length=120, color=(1,0,0)):
        direction = direction / np.linalg.norm(direction)

    # cylinder (shaft)
        shaft = o3d.geometry.TriangleMesh.create_cylinder(radius=8, height=length*0.7)
        shaft.paint_uniform_color(color)
        shaft.compute_vertex_normals()

    # cone (arrow head)
        head = o3d.geometry.TriangleMesh.create_cone(radius=16, height=length*0.3)
        head.paint_uniform_color(color)
        head.compute_vertex_normals()

    # Align arrow with direction
        z_axis = np.array([0,0,1.0])
        v = np.cross(z_axis, direction)
        c = np.dot(z_axis, direction)

        if np.linalg.norm(v) < 1e-6:
            R = np.eye(3)
        else:
            vx = np.array([[0, -v[2], v[1]],
                       [v[2],  0, -v[0]],
                       [-v[1], v[0], 0]])
            R = np.eye(3) + vx + vx @ vx * (1 / (1 + c))

        shaft.rotate(R, center=[0,0,0])
        head.rotate(R, center=[0,0,0])

        shaft.translate(center)
        head.translate(center + direction * (length*0.7))

        return shaft, head

    arrow_min = arrow(p_min, direction=np.array([0,0,-1]), length=150, color=(1,0,0))
    arrow_max = arrow(p_max, direction=np.array([0,0,1]),  length=150, color=(0,1,0))

# D) Show everything together
    o3d.visualization.draw_geometries([
        pcd_clipped,
        plane,
        cube_min, cube_max,
        panel_min, panel_max,
        arrow_min[0], arrow_min[1],
        arrow_max[0], arrow_max[1]
    ], window_name="Step 7 – BIG VISIBLE Min/Max Markers")

    # ---- краткое summary ----
    print("\n✅ Interpretation for defense:")
    print("1) Loaded & triangulated the boat mesh, computed normals.")
    print("2) Sampled ~15k points → point cloud.")
    print("3) Reconstructed smooth surface via Poisson, removed low-density noise.")
    print("4) Built colorful voxel representation (LEGO style) with one cube per voxel, color = height.")
    print("5) Added reference plane and showed original mesh with plane.")
    print("6) Clipped points by plane (kept one side only).")
    print("7) Colored points by Z, marked minimal & maximal height with spheres and arrows.")


if __name__ == "__main__":
    main()
