# Copyright (c) 2021 Aldo Hoeben / fieldOfView
# MeasureTool is released under the terms of the AGPLv3 or higher.

from UM.Tool import Tool
from UM.Event import Event, MouseEvent
from UM.Math.Vector import Vector
from UM.Scene.Selection import Selection
from UM.Scene.SceneNode import SceneNode
from UM.Logger import Logger
from UM.i18n import i18nCatalog

from cura.CuraApplication import CuraApplication
from cura.Scene.CuraSceneNode import CuraSceneNode

from .MeasurePass import MeasurePass
from .MeasureToolHandle import MeasureToolHandle

from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QVector3D

from math import inf

from typing import cast, List, Optional


class MeasureTool(Tool):
    def __init__(self, parent=None) -> None:
        super().__init__()

        self._application = CuraApplication.getInstance()
        self._controller = self.getController()
        self._measure_passes = []  # type: List[MeasurePass]
        self._measure_passes_dirty = True

        self._toolbutton_item = None  # type: Optional[QObject]
        self._tool_enabled = False
        self._dragging = False

        self._i18n_catalog = i18nCatalog("cura")

        self._points = [QVector3D(), QVector3D()]
        self._active_point = 0

        self._handle = (
            MeasureToolHandle()
        )  # type: MeasureToolHandle #Because for some reason MyPy thinks this variable contains Optional[ToolHandle].
        self._handle.setTool(self)

        self.setExposedProperties("PointA", "PointB", "Distance", "ActivePoint")

        self._application.engineCreatedSignal.connect(self._onEngineCreated)
        Selection.selectionChanged.connect(self._onSelectionChanged)
        self._controller.activeStageChanged.connect(self._onActiveStageChanged)
        self._controller.getScene().sceneChanged.connect(self._onSceneChanged)

        self._selection_tool = None  # type: Optional[Tool]

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
        main_window.widthChanged.connect(self._createPickingPass)
        main_window.heightChanged.connect(self._createPickingPass)
        self.propertyChanged.emit()

    def _onSelectionChanged(self) -> None:
        if not self._toolbutton_item:
            return
        self._application.callLater(lambda: self._forceToolEnabled())

    def _onActiveStageChanged(self) -> None:
        self._tool_enabled = self._controller.getActiveStage().stageId == "PrepareStage"
        if not self._tool_enabled:
            self._controller.setSelectionTool(self._selection_tool)
            if self._controller.getActiveTool() == self:
                self._controller.setActiveTool(self._getFallbackTool())
        self._forceToolEnabled()

    def _onSceneChanged(self, node: SceneNode) -> None:
        if node == self._handle:
            return

        self._measure_passes_dirty = True

    def _findToolbarIcon(self, rootItem: QObject) -> Optional[QObject]:
        for child in rootItem.childItems():
            class_name = child.metaObject().className()
            if class_name.startswith("ToolbarButton_QMLTYPE") and child.property(
                "text"
            ) == self._i18n_catalog.i18nc("@label", "Measure"):
                return child
            elif (
                class_name.startswith("QQuickItem")
                or class_name.startswith("QQuickColumn")
                or class_name.startswith("Toolbar_QMLTYPE")
            ):
                found = self._findToolbarIcon(child)
                if found:
                    return found
        return None

    def _forceToolEnabled(self, passive=False) -> None:
        if not self._toolbutton_item:
            return
        try:
            if self._tool_enabled:
                self._toolbutton_item.setProperty("enabled", True)
                if self._application._previous_active_tool == "MeasureTool" and not passive:
                    self._controller.setActiveTool(self._application._previous_active_tool)
            else:
                self._toolbutton_item.setProperty("enabled", False)
                if self._controller.getActiveTool() == self and not passive:
                    self._controller.setActiveTool(self._getFallbackTool())
        except RuntimeError:
            Logger.log("w", "The toolbutton item seems to have gone missing; trying to find it back.")
            main_window = self._application.getMainWindow()
            if not main_window:
                return

            self._toolbutton_item = self._findToolbarIcon(main_window.contentItem())


    def event(self, event: Event) -> bool:
        result = super().event(event)

        if not self._tool_enabled:
            return result

        # overridden from ToolHandle.event(), because we also want to show the handle when there is no selection
        # disabling the tool oon Event.ToolDeactivateEvent is properly handled in ToolHandle.evemt()
        if event.type == Event.ToolActivateEvent:
            if self._handle:
                self._handle.setParent(self.getController().getScene().getRoot())
                self._handle.setEnabled(True)

            self._selection_tool = self._controller._selection_tool
            self._controller.setSelectionTool(None)

            self._application.callLater(lambda: self._forceToolEnabled(passive=True))

        if event.type == Event.ToolDeactivateEvent:
            self._controller.setSelectionTool(self._selection_tool)

            self._application.callLater(lambda: self._forceToolEnabled(passive=True))

        if (
            event.type == Event.MouseReleaseEvent
            and MouseEvent.LeftButton in cast(MouseEvent, event).buttons
        ):
            self._dragging = False

        if (
            event.type == Event.MousePressEvent
            and MouseEvent.LeftButton in cast(MouseEvent, event).buttons
        ):
            mouse_event = cast(MouseEvent, event)

            if QApplication.keyboardModifiers() & Qt.ShiftModifier:
                if self._active_point == 0:
                    self._active_point = 1
                else:
                    self._active_point = 0
            else:
                distances = []  # type: List[float]
                camera = self._controller.getScene().getActiveCamera()

                for point in self._points:
                    if camera.isPerspective():
                        projected_point = camera.project(
                            Vector(point.x(), point.y(), point.z())
                        )
                    else:
                        # Camera.project() does not work for orthographic views in Cura 4.9 and before, so we calculate our own projection
                        projection = camera.getProjectionMatrix()
                        view = camera.getWorldTransformation()
                        view.invert()

                        position = Vector(point.x(), point.y(), point.z())
                        position = position.preMultiply(view)
                        position = position.preMultiply(projection)

                        projected_point = (position.x, position.y)
                    dx = projected_point[0] - (
                        (
                            camera.getWindowSize()[0]
                            * (mouse_event.x + 1)
                            / camera.getViewportWidth()
                        )
                        - 1
                    )
                    dy = projected_point[1] + mouse_event.y
                    distances.append(dx * dx + dy * dy)

                self._active_point = 0
                if distances[1] < distances[0]:
                    self._active_point = 1

            self._dragging = True
            result = self._handle_mouse_event(event, result)

        if event.type == Event.MouseMoveEvent:
            if self._dragging:
                result = self._handle_mouse_event(event, result)

        if self._selection_tool:
            self._selection_tool.event(event)

        return result

    def _handle_mouse_event(self, event: Event, result: bool) -> bool:
        if not self._measure_passes:
            self._createPickingPass()
        if not self._measure_passes:
            return False

        picked_coordinate = []
        mouse_event = cast(MouseEvent, event)

        for axis in self._measure_passes:
            if self._measure_passes_dirty:
                axis.render()

            axis_value = axis.getPickedCoordinate(mouse_event.x, mouse_event.y)
            if axis_value == inf:
                return False
            picked_coordinate.append(axis_value)
        self._measure_passes_dirty = False

        self._points[self._active_point] = QVector3D(*picked_coordinate)

        self._controller.getScene().sceneChanged.emit(self._handle)
        self.propertyChanged.emit()

        return result

    def _createPickingPass(self, *args, **kwargs) -> None:
        active_camera = self._controller.getScene().getActiveCamera()
        if not active_camera:
            return
        viewport_width = active_camera.getViewportWidth()
        viewport_height = active_camera.getViewportHeight()

        self._measure_passes.clear()
        try:
            # Create a set of passes for picking a world-space location from the mouse location
            for axis in range(0, 3):
                self._measure_passes.append(
                    MeasurePass(viewport_width, viewport_height, axis)
                )
        except:
            pass

        self._measure_passes_dirty = True

    def _getFallbackTool(self) -> str:
        try:
            return self._controller._fallback_tool
        except AttributeError:
            return "TranslateTool"