# Copyright (c) 2022 Aldo Hoeben / fieldOfView
# MeasureTool is released under the terms of the AGPLv3 or higher.

from . import MeasureTool

from UM.Version import Version
from UM.Application import Application
from UM.i18n import i18nCatalog

i18n_catalog = i18nCatalog("cura")


def getMetaData():
    cura_version = Version(Application.getInstance().getVersion())

    tool_icon_path = "resources/icons/tool_icon.svg"
    if cura_version < Version("4.11.0") and cura_version.getMajor() > 0:
        tool_icon_path = "resources/icons/tool_icon_legacy.svg"

    tool_panel_path = "resources/qml/MeasureTool.qml"
    if cura_version < Version("5.0.0") and cura_version.getMajor() > 0:
        tool_panel_path = "resources/qml_qt5/MeasureTool.qml"

    metadata = {
        "tool": {
            "name": i18n_catalog.i18nc("@label", "Measure"),
            "description": i18n_catalog.i18nc(
                "@info:tooltip", "Measure parts of objects."
            ),
            "icon": tool_icon_path,
            "tool_panel": tool_panel_path,
            "weight": 6,
        }
    }

    return metadata

def register(app):
    return {"tool": MeasureTool.MeasureTool()}
