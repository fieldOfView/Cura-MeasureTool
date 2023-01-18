// Copyright (c) 2022 Aldo Hoeben / fieldOfView
// MeasureTool is released under the terms of the AGPLv3 or higher.

import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3

import UM 1.1 as UM

Item
{
    id: base
    width: childrenRect.width
    height: childrenRect.height
    UM.I18nCatalog { id: catalog; name: "measuretool"}
    property real unitFactor: UM.Preferences.getValue("measuretool/unit_factor")

    function formatMeasurement(input)
    {
        var decimals = 3;
        if (unitFactor < 0.005) {
            decimals = 0;
        }

        // First convert to fixed-point notation to round the number to 4 decimals and not introduce new floating point errors.
        // Then convert to a string (is implicit). The fixed-point notation will be something like "3.200".
        // Then remove any trailing zeroes and the radix.
        var output = "";
        if (input !== undefined)
        {
            output = (input / unitFactor).toFixed(decimals);
            if (decimals > 0 )
			{
                output = output.replace(/\.?0*$/, "");  // Match on periods, if any ( \.? ), followed by any number of zeros ( 0* ), then the end of string ( $ ).
			}
		}
        if (output == "-0" || output == "")
        {
            output = "0";
        }
        return output;
    }

    GridLayout
    {
        id: textfields

        anchors.leftMargin: UM.Theme.getSize("default_margin").width
        anchors.top: parent.top

        columns: 4
        columnSpacing: Math.round(UM.Theme.getSize("default_margin").width / 2)
        rowSpacing: columnSpacing

        property var pointA: UM.ActiveTool.properties.getValue("PointA")
        property var pointB: UM.ActiveTool.properties.getValue("PointB")
        property var distance: UM.ActiveTool.properties.getValue("Distance")

        Item { width: height; height: UM.Theme.getSize("setting_control").height }

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("@label", "From")
            font: UM.ActiveTool.properties.getValue("ActivePoint") == 0 ? UM.Theme.getFont("default_bold") : UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("@label", "To")
            font: UM.ActiveTool.properties.getValue("ActivePoint") == 1 ? UM.Theme.getFont("default_bold") : UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("@label", "Distance")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
            text: "X"
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("x_axis")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.formatMeasurement(parent.pointA.x)
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.formatMeasurement(parent.pointB.x)
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.formatMeasurement(Math.abs(parent.distance.x))
        }

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
            text: "Y"
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("z_axis") // This is intentional. The internal axis are switched.
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.formatMeasurement(parent.pointA.z)
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.formatMeasurement(parent.pointB.z)
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.formatMeasurement(Math.abs(parent.distance.z))
        }

        Label
        {
            height: UM.Theme.getSize("setting_control").height;
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
            text: "Z";
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("y_axis") // This is intentional. The internal axis are switched.
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.formatMeasurement(parent.pointA.y)
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.formatMeasurement(parent.pointB.y)
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.formatMeasurement(Math.abs(parent.distance.y))
        }


        Label
        {
            height: UM.Theme.getSize("setting_control").height
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
            text: catalog.i18nc("@label", "Diagonal")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text") // This is intentional. The internal axis are switched.
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
        }

        Item { width: height; height: UM.Theme.getSize("setting_control").height; Layout.columnSpan:2 }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.formatMeasurement(parent.distance.length())
        }

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
            text: catalog.i18nc("@label", "Unit")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text") // This is intentional. The internal axis are switched.
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
        }

        ListModel
        {
            id: unitsList
            Component.onCompleted:
            {
                append({ text: catalog.i18nc("@option:unit", "Micron"), factor: 0.001 })
                append({ text: catalog.i18nc("@option:unit", "Millimeter (default)"), factor: 1 })
                append({ text: catalog.i18nc("@option:unit", "Centimeter"), factor: 10 })
                append({ text: catalog.i18nc("@option:unit", "Meter"), factor: 1000 })
                append({ text: catalog.i18nc("@option:unit", "Inch"), factor: 25.4 })
                append({ text: catalog.i18nc("@option:unit", "Feet"), factor: 304.8 })
            }
        }


		ComboBox {
			id: unitDropDownButton
			
			Layout.columnSpan:3
			Layout.fillWidth: true
			
			model: unitsList
			
			textRole: "text"
			
			font: UM.Theme.getFont("default")
			
			height: UM.Theme.getSize("combobox").height
			width: UM.Theme.getSize("combobox").width

            currentIndex:
            {
                var currentChoice = UM.Preferences.getValue("measuretool/unit_factor");
                for(var i = 0; i < unitsList.count; ++i)
                {
                    if(model.get(i).factor == currentChoice)
                    {
                        return i
                    }
                }
            }

            onActivated:
            {
                base.unitFactor = model.get(index).factor;
                UM.Preferences.setValue("measuretool/unit_factor", base.unitFactor)
            }
			
		}
		
    }
}
