import open3d as o3d
import numpy as np
import argparse

def main():
    parser = argparse.ArgumentParser(description="Assignment 5 — Part 1 & 2")
    parser.add_argument("model_path", help="Path to 3D file (ply/obj/stl, etc.)")
    args = parser.parse_args()

    # === Step 1: Load original mesh ===
    mesh = o3d.io.read_triangle_mesh(args.model_path)
    mesh.compute_vertex_normals()

    print("\nStep 1: Original Mesh")
    print(f"Vertices: {len(mesh.vertices)}")
    print(f"Triangles: {len(mesh.triangles)}")
    print(f"Has colors: {mesh.has_vertex_colors()}")
    print(f"Has normals: {mesh.has_vertex_normals()}")
    print(f"Has textures/materials: {mesh.has_textures()}")

    o3d.visualization.draw_geometries([mesh], window_name="Original Model")

    # === Step 2: Sampling to Point Cloud ===
    print("\nStep 2: Sampling to Point Cloud")
    pcd = mesh.sample_points_poisson_disk(10000)  # 10 000 точек

    print(f"Points: {len(pcd.points)}")
    print(f"Has colors: {pcd.has_colors()}")
    print(f"Has normals: {pcd.has_normals()}")

    o3d.visualization.draw_geometries([pcd], window_name="Point Cloud")


        # === Step 3: Surface Reconstruction ===
    print("\nStep 3: Surface Reconstruction")

    # Используем Poisson Reconstruction (восстановление поверхности)
    mesh_rec, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=6)

    # Очистим низкоплотные области, чтобы убрать шум
    densities = np.asarray(densities)
    density_threshold = np.quantile(densities, 0.02)
    vertices_to_keep = densities > density_threshold
    mesh_rec = mesh_rec.select_by_index(np.where(vertices_to_keep)[0])

    # Вычисляем нормали для визуализации
    mesh_rec.compute_vertex_normals()

    print(f"Reconstructed mesh: {len(mesh_rec.vertices)} vertices, {len(mesh_rec.triangles)} triangles")

    o3d.visualization.draw_geometries([mesh_rec], window_name="Step 3: Reconstructed Surface")


        # === Step 4: Mesh Simplification ===
    print("\nStep 4: Mesh Simplification")

    # Уменьшаем количество треугольников в 3 раза
    target_triangles = len(mesh_rec.triangles) // 3
    mesh_simplified = mesh_rec.simplify_quadric_decimation(target_triangles)

    # Пересчитываем нормали
    mesh_simplified.compute_vertex_normals()

    print(f"Simplified mesh: {len(mesh_simplified.vertices)} vertices, {len(mesh_simplified.triangles)} triangles")

    # Визуализация
    o3d.visualization.draw_geometries(
        [mesh_simplified],
        window_name="Step 4: Simplified Mesh"
    )


        # === Step 5: Voxelization ===
    print("\nStep 5: Voxelization")

    # Преобразуем упрощённую сетку в облако точек (для равномерного заполнения)
    pcd_from_mesh = mesh_simplified.sample_points_poisson_disk(5000)

    # Создаём воксельную сетку
    voxel_size = 0.1  # размер кубика (можно менять 0.01–0.05)
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd_from_mesh, voxel_size=voxel_size)

    print(f"Voxel size: {voxel_size}")
    print(f"Number of voxels: {len(voxel_grid.get_voxels())}")

    # Визуализация
    o3d.visualization.draw_geometries(
        [voxel_grid],
        window_name="Step 5: Voxelized Model"
    )



if __name__ == "__main__":
    main()

# cd /Users/aygerimkoszhanova/Desktop/docs/db/assignment5
# python assignment5_open3d.py 12219_boat_v2_L2.obj