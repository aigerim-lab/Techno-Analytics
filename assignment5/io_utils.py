import open3d as o3d
from pathlib import Path

def load_mesh(path_str: str) -> o3d.geometry.TriangleMesh:
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    # Open3D сам понимает формат по расширению (ply/obj/stl/…)
    mesh = o3d.io.read_triangle_mesh(str(path))
    if mesh.is_empty():
        raise ValueError(f"Loaded mesh is empty: {path}")
    return mesh
