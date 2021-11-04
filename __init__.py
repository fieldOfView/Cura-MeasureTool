# Copyright (c) 2021 Aldo Hoeben / fieldOfView
# MeasureTool is released under the terms of the AGPLv3 or higher.

from . import MeasureTool

from UM.Version import Version
from UM.Application import Application
from UM.i18n import i18nCatalog

i18n_catalog = i18nCatalog("cura")


def getMetaData():
    metadata = {
        "tool": {
            "name": i18n_catalog.i18nc("@label", "Measure"),
            "description": i18n_catalog.i18nc(
                "@info:tooltip", "Measure parts of objects."
            ),
            "icon": "resources/icons/tool_icon.svg",
            "tool_panel": "resources/qml/MeasureTool.qml",
            "weight": 6,
        }
    }

    cura_version = Version(Application.getInstance().getVersion())
    if cura_version < Version("4.11.0") and cura_version.getMajor() > 0:
        metadata["tool"]["icon"] = "resources/icons/tool_icon_legacy.svg"

    return metadata

def register(app):
    return {"tool": MeasureTool.MeasureTool()}
