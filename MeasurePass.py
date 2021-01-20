# Copyright (c) 2021 Aldo Hoeben / fieldOfView
# MeasureTool is released under the terms of the AGPLv3 or higher.

from typing import Optional, TYPE_CHECKING
import os.path

from cura.CuraApplication import CuraApplication
from UM.Resources import Resources

from UM.View.RenderPass import RenderPass
from UM.View.GL.OpenGL import OpenGL
from UM.View.RenderBatch import RenderBatch

from UM.Math.Matrix import Matrix
from UM.Math.Vector import Vector

from UM.Scene.Iterator.DepthFirstIterator import DepthFirstIterator

if TYPE_CHECKING:
    from UM.View.GL.ShaderProgram import ShaderProgram

##  A RenderPass subclass that renders a the distance of selectable objects from the active camera to a texture.
#   The texture is used to map a 2d location (eg the mouse location) to a world space position
#
#   Note that in order to increase precision, the 24 bit depth value is encoded into all three of the R,G & B channels
class MeasurePass(RenderPass):
    def __init__(self, width: int, height: int, axis: int) -> None:
        super().__init__("picking", width, height)

        self._axis = axis

        self._renderer = CuraApplication.getInstance().getRenderer()

        self._shader = None #type: Optional[ShaderProgram]
        self._scene = CuraApplication.getInstance().getController().getScene()

    def render(self) -> None:
        if not self._shader:
            self._shader = OpenGL.getInstance().createShaderProgram(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "coordinates.shader")
            )

        self._shader.setUniformValue("u_axisId", self._axis)

        width, height = self.getSize()
        self._gl.glViewport(0, 0, width, height)
        self._gl.glClearColor(1.0, 1.0, 1.0, 0.0)
        self._gl.glClear(self._gl.GL_COLOR_BUFFER_BIT | self._gl.GL_DEPTH_BUFFER_BIT)

        # Create a new batch to be rendered
        batch = RenderBatch(self._shader)

        # Fill up the batch with objects that can be sliced. `
        for node in DepthFirstIterator(self._scene.getRoot()): #type: ignore #Ignore type error because iter() should get called automatically by Python syntax.
            if node.callDecoration("isSliceable") and node.getMeshData() and node.isVisible():
                batch.addItem(node.getWorldTransformation(), node.getMeshData())

        z_fight_distance = 0.2  # Distance between buildplate and disallowed area meshes to prevent z-fighting
        buildplate_transform = Matrix()
        buildplate_transform.setToIdentity()
        buildplate_transform.translate(Vector(0, z_fight_distance, 0))
        buildplate_mesh = CuraApplication.getInstance().getBuildVolume()._grid_mesh
        batch.addItem(buildplate_transform, buildplate_mesh)

        self.bind()
        batch.render(self._scene.getActiveCamera())
        self.release()

    ##  Get the distance in mm from the camera to at a certain pixel coordinate.
    def getPickedCoordinate(self, x: int, y: int) -> float:
        output = self.getOutput()

        window_size = self._renderer.getWindowSize()

        px = (0.5 + x / 2.0) * window_size[0]
        py = (0.5 + y / 2.0) * window_size[1]

        if px < 0 or px > (output.width() - 1) or py < 0 or py > (output.height() - 1):
            return -1

        value = output.pixel(px, py) # value in micron, from in r, g & b channels
        value = (value & 0x00ffffff) / 1000. # drop the alpha channel and covert to mm
        value = value - 8388.608 # correct for signedness

        return value

