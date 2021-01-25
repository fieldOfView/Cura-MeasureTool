# Copyright (c) 2020 Aldo Hoeben / fieldOfView
# MeasureTool is released under the terms of the AGPLv3 or higher.

from UM.Mesh.MeshData import MeshData, calculateNormalsFromIndexedVertices
from UM.Scene.ToolHandle import ToolHandle
from UM.Math.Vector import Vector
from UM.View.GL.OpenGL import OpenGL
from UM.Resources import Resources

import trimesh
import numpy

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .MeasureTool import MeasureTool

class MeasureToolHandle(ToolHandle):

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self._name = "MeasureToolHandle"

        self._handle_width = 3

        self._tool = None  # type: Optional[MeasureTool]


    def setTool(self, tool: "MeasureTool") -> None:
        self._tool = tool


    def buildMesh(self) -> None:
        mesh = self._toMeshData(trimesh.creation.icosphere(subdivisions=2,radius = self._handle_width / 2))
        self.setSolidMesh(mesh)


    def render(self, renderer) -> bool:
        if not self._shader:
            self._shader = OpenGL.getInstance().createShaderProgram(Resources.getPath(Resources.Shaders, "toolhandle.shader"))

        if self._solid_mesh and self._tool:
            for position in [self._tool.getPointA(), self._tool.getPointB()]:
                self.setPosition(Vector(position.x(), position.y(), position.z()))
                renderer.queueNode(self, mesh = self._solid_mesh, overlay = False, shader = self._shader)

        return True



    def _toMeshData(self, tri_node: trimesh.base.Trimesh) -> MeshData:
        tri_faces = tri_node.faces
        tri_vertices = tri_node.vertices

        indices = []
        vertices = []

        index_count = 0
        face_count = 0
        for tri_face in tri_faces:
            face = []
            for tri_index in tri_face:
                vertices.append(tri_vertices[tri_index])
                face.append(index_count)
                index_count += 1
            indices.append(face)
            face_count += 1

        vertices = numpy.asarray(vertices, dtype=numpy.float32)
        indices = numpy.asarray(indices, dtype=numpy.int32)
        normals = calculateNormalsFromIndexedVertices(vertices, indices, face_count)

        mesh_data = MeshData(vertices=vertices, indices=indices, normals=normals)

        return mesh_data
