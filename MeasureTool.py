# Copyright (c) 2021 Aldo Hoeben / fieldOfView
# MeasureTool is released under the terms of the AGPLv3 or higher.

from UM.Tool import Tool
from UM.Event import Event, MouseEvent
from UM.Math.Vector import Vector
from UM.Scene.Selection import Selection
from UM.i18n import i18nCatalog

from cura.CuraApplication import CuraApplication
from cura.Scene.CuraSceneNode import CuraSceneNode
from .MeasurePass import MeasurePass
from .MeasureToolHandle import MeasureToolHandle

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QVector3D

from typing import cast, List, Optional

class MeasureTool(Tool):
    def __init__(self, parent = None) -> None:
        super().__init__()

        self._application = CuraApplication.getInstance()
        self._controller = self.getController()
        self._measure_passes = None  # type: Optional[List[MeasurePass]]
        self._toolbutton_item = None  # type: Optional[QObject]

        self._i18n_catalog = i18nCatalog("cura")

        self._points = [QVector3D(), QVector3D()]
        self._active_point = 0

        self.setExposedProperties("PointA", "PointB", "Distance", "ActivePoint")

        self._application.engineCreatedSignal.connect(self._onEngineCreated)
        Selection.selectionChanged.connect(self._onSelectionChanged)

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
        main_window = self._application.getMainWindow()
        if not main_window:
            return

        self._toolbutton_item = self._findToolbarIcon(main_window.contentItem())
        self._forceToolEnabled()

        main_window.viewportRectChanged.connect(self._createPickingPass)
        self.propertyChanged.emit()

    def _onSelectionChanged(self) -> None:
        if not self._toolbutton_item:
            return
        self._application.callLater(lambda: self._forceToolEnabled())

    def _findToolbarIcon(self, rootItem: QObject) -> Optional[QObject]:
        for child in rootItem.childItems():
            class_name = child.metaObject().className()
            if class_name.startswith("ToolbarButton_QMLTYPE") and child.property("text") == self._i18n_catalog.i18nc("@label", "Measure"):
                return child
            elif class_name.startswith("QQuickItem") or class_name.startswith("QQuickColumn") or class_name.startswith("Toolbar_QMLTYPE"):
                found = self._findToolbarIcon(child)
                if found:
                    return found
        return None

    def _forceToolEnabled(self) -> None:
        if not self._toolbutton_item:
            return
        self._toolbutton_item.setProperty("enabled", True)
        if self._application._previous_active_tool == "MeasureTool":
            self._controller.setActiveTool(self._application._previous_active_tool)

    def _createPickingPass(self) -> None:
        active_camera = self._controller.getScene().getActiveCamera()
        if not active_camera:
            return
        viewport_width = active_camera.getViewportWidth()
        viewport_height = active_camera.getViewportHeight()

        try:
            # Create a set of passes for picking a world-space location from the mouse location
            self._measure_passes = []  # type: Optional[List[MeasurePass]]
            for axis in range(0,3):
                self._measure_passes.append(MeasurePass(active_camera.getViewportWidth(), active_camera.getViewportHeight(), axis))
        except:
            self._measure_passes = []  # type: Optional[List[MeasurePass]]

    def event(self, event: Event) -> bool:
        result = super().event(event)

        if event.type == Event.MousePressEvent and MouseEvent.LeftButton in cast(MouseEvent, event).buttons and self._controller.getToolsEnabled():
            if not self._measure_passes:
                self._createPickingPass()
            if not self._measure_passes:
                return result

            picked_coordinate = []
            for axis in self._measure_passes:
                axis.render()
                picked_coordinate.append(axis.getPickedCoordinate(cast(MouseEvent, event).x, cast(MouseEvent, event).y))

            self._points[self._active_point] = QVector3D(*picked_coordinate)
            if self._active_point == 0:
                self._active_point = 1
            else:
                self._active_point = 0

            self.propertyChanged.emit()

        return result
