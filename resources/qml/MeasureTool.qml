// Copyright (c) 2022 Aldo Hoeben / fieldOfView
// MeasureTool is released under the terms of the AGPLv3 or higher.

import QtQuick 2.2
import QtQuick.Controls 2.0

import UM 1.1 as UM

Item
{
    id: base
    width: childrenRect.width
    height: childrenRect.height
    UM.I18nCatalog { id: catalog; name: "cura"}

    function roundFloat(input, decimals)
    {
        //First convert to fixed-point notation to round the number to 4 decimals and not introduce new floating point errors.
        //Then convert to a string (is implicit). The fixed-point notation will be something like "3.200".
        //Then remove any trailing zeroes and the radix.
        var output = "";
        if (input !== undefined)
        {
            output = input.toFixed(decimals).replace(/\.?0*$/, ""); //Match on periods, if any ( \.? ), followed by any number of zeros ( 0* ), then the end of string ( $ ).
        }
        if (output == "-0")
        {
            output = "0";
        }
        return output;
    }

    Grid
    {
        id: textfields;

        anchors.leftMargin: UM.Theme.getSize("default_margin").width;
        anchors.top: parent.top;

        columns: 4;
        flow: Grid.TopToBottom;
        spacing: Math.round(UM.Theme.getSize("default_margin").width / 2);

        property int cellWidth: Math.floor(UM.Theme.getSize("setting_control").width * .4)
        property var pointA: UM.ActiveTool.properties.getValue("PointA")
        property var pointB: UM.ActiveTool.properties.getValue("PointB")
        property var distance: UM.ActiveTool.properties.getValue("Distance")

        Item { width: height; height: UM.Theme.getSize("setting_control").height }

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
            height: UM.Theme.getSize("setting_control").height;
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
            text: "Z";
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("y_axis") // This is intentional. The internal axis are switched.
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
        }

        Item { width: height; height: UM.Theme.getSize("setting_control").height }

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: "From"
            font: UM.ActiveTool.properties.getValue("ActivePoint") == 0 ? UM.Theme.getFont("default_bold") : UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.roundFloat(parent.pointA.x, 3)
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.roundFloat(parent.pointA.z, 3)
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.roundFloat(parent.pointA.y, 3)
        }

        Item { width: height; height: UM.Theme.getSize("setting_control").height }

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: "To"
            font: UM.ActiveTool.properties.getValue("ActivePoint") == 1 ? UM.Theme.getFont("default_bold") : UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.roundFloat(parent.pointB.x, 3)
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.roundFloat(parent.pointB.z, 3)
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.roundFloat(parent.pointB.y, 3)
        }

        Item { width: height; height: UM.Theme.getSize("setting_control").height }

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: "Distance"
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.roundFloat(Math.abs(parent.distance.x), 3)
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.roundFloat(Math.abs(parent.distance.z), 3)
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.roundFloat(Math.abs(parent.distance.y), 3)
        }

        Label
        {
            width: parent.cellWidth
            height: UM.Theme.getSize("setting_control").height
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            text: base.roundFloat(parent.distance.length(), 3)
        }
    }
}
