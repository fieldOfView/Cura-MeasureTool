// Copyright (c) 2016 Ultimaker B.V.
// Uranium is released under the terms of the LGPLv3 or higher.

import QtQuick 2.2
import QtQuick.Controls 1.2

import UM 1.1 as UM

Item
{
    id: base
    width: childrenRect.width
    height: childrenRect.height
    UM.I18nCatalog { id: catalog; name: "uranium"}

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

        columns: 2;
        flow: Grid.TopToBottom;
        spacing: Math.round(UM.Theme.getSize("default_margin").width / 2);

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: "X"
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("x_axis")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: "Y"
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("z_axis") // This is intentional. The internal axis are switched.
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }

        Label
        {
            height: UM.Theme.getSize("setting_control").height;
            text: "Z";
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("y_axis") // This is intentional. The internal axis are switched.
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }
        TextField
        {
            id: xTextField
            width: UM.Theme.getSize("setting_control").width
            height: UM.Theme.getSize("setting_control").height
            property string unit: "mm"
            style: UM.Theme.styles.text_field
            enabled: false
            text: base.roundFloat(UM.ActiveTool.properties.getValue("Position").x, 3)
        }
        TextField
        {
            id: yTextField
            width: UM.Theme.getSize("setting_control").width
            height: UM.Theme.getSize("setting_control").height
            property string unit: "mm"
            style: UM.Theme.styles.text_field
            enabled: false
            text: base.roundFloat(UM.ActiveTool.properties.getValue("Position").z, 3)
        }
        TextField
        {
            id: zTextField
            width: UM.Theme.getSize("setting_control").width
            height: UM.Theme.getSize("setting_control").height
            property string unit: "mm"
            style: UM.Theme.styles.text_field
            enabled: false
            text: base.roundFloat(UM.ActiveTool.properties.getValue("Position").y, 3)
        }
    }
}
