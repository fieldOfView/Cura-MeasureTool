# Copyright (c) 2020 Aldo Hoeben / fieldOfView
# MeasureTool is released under the terms of the AGPLv3 or higher.

from UM.Mesh.MeshBuilder import MeshBuilder
from UM.Scene.ToolHandle import ToolHandle


class MeasureToolHandle(ToolHandle):

    def __init__(self, parent = None):
        super().__init__(parent)
        self._name = "MeasureToolHandle"


    def buildMesh(self):
        mb = MeshBuilder()

        self.setSolidMesh(mb.build())

        mb = MeshBuilder()

        self.setSelectionMesh(mb.build())
