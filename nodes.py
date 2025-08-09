import torch
import numpy as np
import math
from typing import Any, Dict, List, Tuple, Optional
import base64
import json

class PrimitiveMeshGenerator:
    """
    基础几何体mesh生成器
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "shape": (["cube", "sphere", "cylinder", "cone", "plane", "torus"], {
                    "default": "cube"
                }),
                "resolution": ("INT", {
                    "default": 16,
                    "min": 4,
                    "max": 128,
                    "step": 2
                }),
                "scale": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1
                }),
            },
            "optional": {
                "center_x": ("FLOAT", {
                    "default": 0.0,
                    "min": -10.0,
                    "max": 10.0,
                    "step": 0.1
                }),
                "center_y": ("FLOAT", {
                    "default": 0.0,
                    "min": -10.0,
                    "max": 10.0,
                    "step": 0.1
                }),
                "center_z": ("FLOAT", {
                    "default": 0.0,
                    "min": -10.0,
                    "max": 10.0,
                    "step": 0.1
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("mesh_vertices", "mesh_faces", "vertex_count")
    FUNCTION = "generate_mesh"
    CATEGORY = "mesh_generation"
    
    def generate_mesh(self, shape: str, resolution: int, scale: float, 
                     center_x: float = 0.0, center_y: float = 0.0, center_z: float = 0.0) -> Tuple[str, str, int]:
        """生成基础几何体mesh"""
        center = np.array([center_x, center_y, center_z])
        
        if shape == "cube":
            vertices, faces = self._generate_cube(scale, center)
        elif shape == "sphere":
            vertices, faces = self._generate_sphere(resolution, scale, center)
        elif shape == "cylinder":
            vertices, faces = self._generate_cylinder(resolution, scale, center)
        elif shape == "cone":
            vertices, faces = self._generate_cone(resolution, scale, center)
        elif shape == "plane":
            vertices, faces = self._generate_plane(resolution, scale, center)
        elif shape == "torus":
            vertices, faces = self._generate_torus(resolution, scale, center)
        else:
            vertices, faces = self._generate_cube(scale, center)
        
        # 转换为JSON字符串
        vertices_json = json.dumps(vertices.tolist())
        faces_json = json.dumps(faces.tolist())
        
        return (vertices_json, faces_json, len(vertices))
    
    def _generate_cube(self, scale: float, center: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """生成立方体"""
        s = scale / 2
        vertices = np.array([
            [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],  # bottom
            [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]       # top
        ]) + center
        
        faces = np.array([
            [0, 1, 2], [0, 2, 3],  # bottom
            [4, 7, 6], [4, 6, 5],  # top
            [0, 4, 5], [0, 5, 1],  # front
            [2, 6, 7], [2, 7, 3],  # back
            [0, 3, 7], [0, 7, 4],  # left
            [1, 5, 6], [1, 6, 2]   # right
        ])
        
        return vertices, faces
    
    def _generate_sphere(self, resolution: int, scale: float, center: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """生成球体"""
        vertices = []
        faces = []
        
        for i in range(resolution + 1):
            lat = math.pi * (-0.5 + i / resolution)
            for j in range(resolution):
                lon = 2 * math.pi * j / resolution
                
                x = scale * math.cos(lat) * math.cos(lon)
                y = scale * math.cos(lat) * math.sin(lon)
                z = scale * math.sin(lat)
                
                vertices.append([x + center[0], y + center[1], z + center[2]])
        
        for i in range(resolution):
            for j in range(resolution):
                curr = i * resolution + j
                next_i = ((i + 1) % (resolution + 1)) * resolution + j
                next_j = i * resolution + (j + 1) % resolution
                next_ij = ((i + 1) % (resolution + 1)) * resolution + (j + 1) % resolution
                
                if i < resolution:
                    faces.append([curr, next_i, next_ij])
                    faces.append([curr, next_ij, next_j])
        
        return np.array(vertices), np.array(faces)
    
    def _generate_cylinder(self, resolution: int, scale: float, center: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """生成圆柱体"""
        vertices = []
        faces = []
        
        # 底部圆心
        vertices.append([center[0], center[1], center[2] - scale/2])
        # 顶部圆心
        vertices.append([center[0], center[1], center[2] + scale/2])
        
        # 底部圆周顶点
        for i in range(resolution):
            angle = 2 * math.pi * i / resolution
            x = scale/2 * math.cos(angle) + center[0]
            y = scale/2 * math.sin(angle) + center[1]
            vertices.append([x, y, center[2] - scale/2])
        
        # 顶部圆周顶点
        for i in range(resolution):
            angle = 2 * math.pi * i / resolution
            x = scale/2 * math.cos(angle) + center[0]
            y = scale/2 * math.sin(angle) + center[1]
            vertices.append([x, y, center[2] + scale/2])
        
        # 底面三角形
        for i in range(resolution):
            faces.append([0, 2 + i, 2 + (i + 1) % resolution])
        
        # 顶面三角形
        for i in range(resolution):
            faces.append([1, 2 + resolution + (i + 1) % resolution, 2 + resolution + i])
        
        # 侧面
        for i in range(resolution):
            next_i = (i + 1) % resolution
            bottom_curr = 2 + i
            bottom_next = 2 + next_i
            top_curr = 2 + resolution + i
            top_next = 2 + resolution + next_i
            
            faces.append([bottom_curr, bottom_next, top_next])
            faces.append([bottom_curr, top_next, top_curr])
        
        return np.array(vertices), np.array(faces)
    
    def _generate_cone(self, resolution: int, scale: float, center: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """生成圆锥体"""
        vertices = []
        faces = []
        
        # 底部圆心
        vertices.append([center[0], center[1], center[2] - scale/2])
        # 顶点
        vertices.append([center[0], center[1], center[2] + scale/2])
        
        # 底部圆周顶点
        for i in range(resolution):
            angle = 2 * math.pi * i / resolution
            x = scale/2 * math.cos(angle) + center[0]
            y = scale/2 * math.sin(angle) + center[1]
            vertices.append([x, y, center[2] - scale/2])
        
        # 底面三角形
        for i in range(resolution):
            faces.append([0, 2 + i, 2 + (i + 1) % resolution])
        
        # 侧面三角形
        for i in range(resolution):
            faces.append([1, 2 + (i + 1) % resolution, 2 + i])
        
        return np.array(vertices), np.array(faces)
    
    def _generate_plane(self, resolution: int, scale: float, center: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """生成平面"""
        vertices = []
        faces = []
        
        step = scale / resolution
        start = -scale / 2
        
        for i in range(resolution + 1):
            for j in range(resolution + 1):
                x = start + i * step + center[0]
                y = start + j * step + center[1]
                z = center[2]
                vertices.append([x, y, z])
        
        for i in range(resolution):
            for j in range(resolution):
                curr = i * (resolution + 1) + j
                next_i = (i + 1) * (resolution + 1) + j
                next_j = i * (resolution + 1) + (j + 1)
                next_ij = (i + 1) * (resolution + 1) + (j + 1)
                
                faces.append([curr, next_i, next_ij])
                faces.append([curr, next_ij, next_j])
        
        return np.array(vertices), np.array(faces)
    
    def _generate_torus(self, resolution: int, scale: float, center: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """生成环面"""
        vertices = []
        faces = []
        
        major_radius = scale / 2
        minor_radius = scale / 4
        
        for i in range(resolution):
            for j in range(resolution):
                u = 2 * math.pi * i / resolution
                v = 2 * math.pi * j / resolution
                
                x = (major_radius + minor_radius * math.cos(v)) * math.cos(u) + center[0]
                y = (major_radius + minor_radius * math.cos(v)) * math.sin(u) + center[1]
                z = minor_radius * math.sin(v) + center[2]
                
                vertices.append([x, y, z])
        
        for i in range(resolution):
            for j in range(resolution):
                curr = i * resolution + j
                next_i = ((i + 1) % resolution) * resolution + j
                next_j = i * resolution + (j + 1) % resolution
                next_ij = ((i + 1) % resolution) * resolution + (j + 1) % resolution
                
                faces.append([curr, next_i, next_ij])
                faces.append([curr, next_ij, next_j])
        
        return np.array(vertices), np.array(faces)


class MeshTransform:
    """
    Mesh变换节点
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mesh_vertices": ("STRING",),
                "rotation_x": ("FLOAT", {
                    "default": 0.0,
                    "min": -360.0,
                    "max": 360.0,
                    "step": 1.0
                }),
                "rotation_y": ("FLOAT", {
                    "default": 0.0,
                    "min": -360.0,
                    "max": 360.0,
                    "step": 1.0
                }),
                "rotation_z": ("FLOAT", {
                    "default": 0.0,
                    "min": -360.0,
                    "max": 360.0,
                    "step": 1.0
                }),
                "scale_x": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1
                }),
                "scale_y": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1
                }),
                "scale_z": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("transformed_vertices",)
    FUNCTION = "transform_mesh"
    CATEGORY = "mesh_generation"
    
    def transform_mesh(self, mesh_vertices: str, rotation_x: float, rotation_y: float, rotation_z: float,
                      scale_x: float, scale_y: float, scale_z: float) -> Tuple[str]:
        """对mesh进行变换"""
        vertices = np.array(json.loads(mesh_vertices))
        
        # 缩放
        scale_matrix = np.array([scale_x, scale_y, scale_z])
        vertices = vertices * scale_matrix
        
        # 旋转
        vertices = self._rotate_vertices(vertices, rotation_x, rotation_y, rotation_z)
        
        return (json.dumps(vertices.tolist()),)
    
    def _rotate_vertices(self, vertices: np.ndarray, rx: float, ry: float, rz: float) -> np.ndarray:
        """旋转顶点"""
        # 转换为弧度
        rx = math.radians(rx)
        ry = math.radians(ry)
        rz = math.radians(rz)
        
        # X轴旋转矩阵
        if rx != 0:
            rot_x = np.array([
                [1, 0, 0],
                [0, math.cos(rx), -math.sin(rx)],
                [0, math.sin(rx), math.cos(rx)]
            ])
            vertices = vertices @ rot_x.T
        
        # Y轴旋转矩阵
        if ry != 0:
            rot_y = np.array([
                [math.cos(ry), 0, math.sin(ry)],
                [0, 1, 0],
                [-math.sin(ry), 0, math.cos(ry)]
            ])
            vertices = vertices @ rot_y.T
        
        # Z轴旋转矩阵
        if rz != 0:
            rot_z = np.array([
                [math.cos(rz), -math.sin(rz), 0],
                [math.sin(rz), math.cos(rz), 0],
                [0, 0, 1]
            ])
            vertices = vertices @ rot_z.T
        
        return vertices


class MeshExporter:
    """
    Mesh导出节点
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mesh_vertices": ("STRING",),
                "mesh_faces": ("STRING",),
                "format": (["obj", "ply"], {
                    "default": "obj"
                }),
                "filename": ("STRING", {
                    "default": "mesh_output",
                    "multiline": False
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_content",)
    FUNCTION = "export_mesh"
    CATEGORY = "mesh_generation"
    
    def export_mesh(self, mesh_vertices: str, mesh_faces: str, format: str, filename: str) -> Tuple[str]:
        """导出mesh为文件格式"""
        vertices = np.array(json.loads(mesh_vertices))
        faces = np.array(json.loads(mesh_faces))
        
        if format == "obj":
            content = self._export_obj(vertices, faces)
        elif format == "ply":
            content = self._export_ply(vertices, faces)
        else:
            content = self._export_obj(vertices, faces)
        
        return (content,)
    
    def _export_obj(self, vertices: np.ndarray, faces: np.ndarray) -> str:
        """导出为OBJ格式"""
        lines = ["# OBJ file generated by ComfyUI Mesh Nodes", ""]
        
        # 写入顶点
        for vertex in vertices:
            lines.append(f"v {vertex[0]:.6f} {vertex[1]:.6f} {vertex[2]:.6f}")
        
        lines.append("")
        
        # 写入面（OBJ格式使用1-based索引）
        for face in faces:
            lines.append(f"f {face[0]+1} {face[1]+1} {face[2]+1}")
        
        return "\n".join(lines)
    
    def _export_ply(self, vertices: np.ndarray, faces: np.ndarray) -> str:
        """导出为PLY格式"""
        lines = [
            "ply",
            "format ascii 1.0",
            f"element vertex {len(vertices)}",
            "property float x",
            "property float y", 
            "property float z",
            f"element face {len(faces)}",
            "property list uchar int vertex_indices",
            "end_header"
        ]
        
        # 写入顶点
        for vertex in vertices:
            lines.append(f"{vertex[0]:.6f} {vertex[1]:.6f} {vertex[2]:.6f}")
        
        # 写入面
        for face in faces:
            lines.append(f"3 {face[0]} {face[1]} {face[2]}")
        
        return "\n".join(lines)


# 节点映射配置
NODE_CLASS_MAPPINGS = {
    "PrimitiveMeshGenerator": PrimitiveMeshGenerator,
    "MeshTransform": MeshTransform,
    "MeshExporter": MeshExporter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PrimitiveMeshGenerator": "Primitive Mesh Generator",
    "MeshTransform": "Mesh Transform",
    "MeshExporter": "Mesh Exporter",
}