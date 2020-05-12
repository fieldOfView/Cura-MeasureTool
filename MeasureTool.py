# Copyright (c) 2020 fieldOfView
# MeasureTool is released under the terms of the AGPLv3 or higher.

from UM.Tool import Tool
from UM.Event import Event, MouseEvent

from cura.CuraApplication import CuraApplication
from cura.Scene.CuraSceneNode import CuraSceneNode
from .MeassurePass import MeasurePass

class MeasureTool(Tool):
    def __init__(self, parent = None) -> None:
        super().__init__()

        self._application = CuraApplication.getInstance()
        self._controller = self.getController()

    def event(self, event):
        super().event(event)

        if event.type == Event.MousePressEvent and MouseEvent.LeftButton in event.buttons and self._controller.getToolsEnabled():
            # Create a pass for picking a world-space location from the mouse location
            active_camera = self._controller.getScene().getActiveCamera()
            picking_pass = MeassurePass(active_camera.getViewportWidth(), active_camera.getViewportHeight())
            picking_pass.render()

            picked_distance = picking_pass.getPickedDepth(event.x, event.y)
            picked_position = picking_pass.getPickedPosition(event.x, event.y)

            print(picked_distance, picked_position)