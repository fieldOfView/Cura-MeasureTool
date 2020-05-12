# Copyright (c) 2020 Aldo Hoeben / fieldOfView
# MeasureTool is released under the terms of the AGPLv3 or higher.

from . import MeasureTool

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("cura")

def getMetaData():
    return {
        "tool": {
            "name": i18n_catalog.i18nc("@label", "Measure"),
            "description": i18n_catalog.i18nc("@info:tooltip", "Measure parts of objects."),
            "icon": "tool_icon.svg",
            "weight": 5
        }
    }

def register(app):
    return { "tool": MeasureTool.MeasureTool() }
