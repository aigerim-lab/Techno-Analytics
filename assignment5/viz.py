# viz.py
import open3d as o3d

def show_mesh(mesh: o3d.geometry.TriangleMesh, window_name: str = "Model"):
    # простое окно просмотра
    o3d.visualization.draw_geometries([mesh], window_name=window_name)
