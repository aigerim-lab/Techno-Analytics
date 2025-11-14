import open3d as o3d

def ensure_normals(mesh: o3d.geometry.TriangleMesh) -> None:
    # Если нормалей нет — посчитаем (для корретного отображения света/шейдинга)
    if not mesh.has_vertex_normals():
        mesh.compute_vertex_normals()

def print_mesh_info(mesh: o3d.geometry.TriangleMesh, title: str = "Original Mesh") -> None:
    n_vertices = len(mesh.vertices)
    n_tris     = len(mesh.triangles)
    has_colors = mesh.has_vertex_colors()
    has_norms  = mesh.has_vertex_normals()
    has_tex    = mesh.has_textures()  # часто False для STL/OBJ без материалов

    print(f"\n{title}")
    print(f"Vertices:   {n_vertices}")
    print(f"Triangles:  {n_tris}")
    print(f"Has colors: {has_colors}")
    print(f"Has normals:{has_norms}")
    print(f"Has textures/materials: {has_tex}")
