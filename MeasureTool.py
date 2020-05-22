# Copyright (c) 2020 fieldOfView
# MeasureTool is released under the terms of the AGPLv3 or higher.

from UM.Tool import Tool
from UM.Event import Event, MouseEvent
from UM.Math.Vector import Vector

from cura.CuraApplication import CuraApplication
from cura.Scene.CuraSceneNode import CuraSceneNode
from .MeasurePass import MeasurePass

from typing import List, Optional

from PyQt5.QtGui import QVector3D

class MeasureTool(Tool):
    def __init__(self, parent = None) -> None:
        super().__init__()

        self._application = CuraApplication.getInstance()
        self._controller = self.getController()
        self._measure_passes = None  # type: Optional[List[MeasurePass]]

        self._points = [QVector3D(), QVector3D()]
        self._active_point = 0

        self._application.engineCreatedSignal.connect(self._onEngineCreated)

        self.setExposedProperties("PointA", "PointB", "Distance", "ActivePoint")

    def getPointA(self) -> QVector3D:
        return self._points[0]

    def getPointB(self) -> QVector3D:
        return self._points[1]

    def getDistance(self) -> QVector3D:
        return self._points[1] - self._points[0]

    def getActivePoint(self) -> int:
        return self._active_point

    def setActivePoint(self, active_point: int) -> None:
        if active_point != self._active_point:
            self._active_point = active_point
            self.propertyChanged.emit()

    def _onEngineCreated(self) -> None:
        self._application.getMainWindow().viewportRectChanged.connect(self._createPickingPass)
        self.propertyChanged.emit()

    def _createPickingPass(self) -> None:
        active_camera = self._controller.getScene().getActiveCamera()
        viewport_width = active_camera.getViewportWidth()
        viewport_height = active_camera.getViewportHeight()

        try:
            # Create a set of passes for picking a world-space location from the mouse location
            self._measure_passes = []  # type: Optional[List[MeassurePass]]
            for axis in range(0,3):
                self._measure_passes.append(MeasurePass(active_camera.getViewportWidth(), active_camera.getViewportHeight(), axis))
        except:
            self._measure_passes = []  # type: Optional[List[MeassurePass]]

    def event(self, event) -> None:
        super().event(event)

        if event.type == Event.MousePressEvent and MouseEvent.LeftButton in event.buttons and self._controller.getToolsEnabled():
            if not self._measure_passes:
                self._createPickingPass()
            if not self._measure_passes:
                return

            picked_coordinate = []
            for axis in self._measure_passes:
                axis.render()
                picked_coordinate.append(axis.getPickedCoordinate(event.x, event.y))

            self._points[self._active_point] = QVector3D(*picked_coordinate)
            if self._active_point == 0:
                self._active_point = 1
            else:
                self._active_point = 0

            self.propertyChanged.emit()
