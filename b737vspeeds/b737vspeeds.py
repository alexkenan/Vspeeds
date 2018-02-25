#!/usr/bin/env python3
"""
Calculate V1, VR, and V2 for Boeing 737-700 and Boeing 737-800 aircraft
based on estimates from http://www.b737.org.uk/vspeedcalc2.htm

DO NOT USE FOR FLIGHT PLANNING
"""
#####################################
#    LAST UPDATED     22 FEB 2017   #
#####################################
from appJar import gui


def v1(takeoff_weight: float, velocity_2: int) -> int:
    """
    Calculate V1 for a Boeing 737-700 or 737-800

    Method:
        Difference between V1 and V2 varies with the weight:

        65t       10kts,
        60t       11kts,
        55t       12kts,
        50t       13kts,
        45t       15kts,
        40t       17kts,

    :param takeoff_weight: aircraft takeoff weight in metric tons (float)
    :param velocity_2: V2 in knots (int)
    :return: velocity in knots (int)
    """
    if takeoff_weight >= 65.0:
        return velocity_2 - 10
    elif 65.0 > takeoff_weight >= 60.0:
        return velocity_2 - 11
    elif 60.0 > takeoff_weight >= 55.0:
        return velocity_2 - 12
    elif 55.0 > takeoff_weight >= 50.0:
        return velocity_2 - 13
    elif 50.0 > takeoff_weight >= 45.0:
        return velocity_2 - 15
    else:
        return velocity_2 - 17


def vr(takeoff_weight: float, velocity_1: int) -> int:
    """
    Calculate VR from takeoff weight and V1

    Method:
        The difference between V1 and Vr is just 2 kts up to landing weight of 55t.
        Above this weight, this difference is 4kts.

    :param takeoff_weight: aircraft takeoff weight in metric tons (float)
    :param velocity_1: V1 in knots (int)
    :return: VR in knots (int)
    """
    if takeoff_weight > 55.0:
        return velocity_1 + 4
    else:
        return velocity_1 + 2


def v2(takeoff_weight):
    """
    Calculate V2 for a Boeing 737-700 or 737-800

    Method:
        737-700: V2 is Takeoff Weight (TOW) - 25
        737-800: V2 is TOW - 20

    :param takeoff_weight: takeoff weight in metric tons (float)
    :return: V2 in knots (int)
    """
    if app.getRadioButton("airplane_variant") == 'Boeing 737-700':
        temp_v = round(takeoff_weight - 25, 0)
        temp = float('1{}'.format(temp_v))
        return int(temp)
    else:
        temp_v = round(takeoff_weight - 20, 0)
        temp = float('1{}'.format(temp_v))
        return int(temp)


def convert_lbs_to_metric_tons(weight):
    """
    Convert aircraft weight from lbs to metric tons
    :param weight: aircraft weight in lbs
    :return: aircraft weight in metric tons (kg)
    """
    return round(weight*0.000453592, 1)


def press(btn) -> None:
    if btn == "Cancel":
        app.stop()
    else:
        aircraft_weight = app.getEntry("weight")
        if app.getRadioButton("airplane_variant") == 'Boeing 737-700':
            if aircraft_weight > 154500:
                app.setLabel("v2_label", 'MTOW = 154,500 lb')
                app.setLabel("v1_label", 'MTOW = 154,500 lb')
                app.setLabel("vr_label", 'MTOW = 154,500 lb')
                return
        else:
            if aircraft_weight > 174200:
                app.setLabel("v2_label", 'MTOW = 154,500 lb')
                app.setLabel("v1_label", 'MTOW = 154,500 lb')
                app.setLabel("vr_label", 'MTOW = 154,500 lb')
                return

        aircraft_weight_tons = convert_lbs_to_metric_tons(aircraft_weight)
        velocity_2 = v2(aircraft_weight_tons)
        app.setLabel("v2_label", '{} knots'.format(velocity_2))
        velocity_1 = v1(aircraft_weight_tons, velocity_2)
        app.setLabel("v1_label", '{} knots'.format(velocity_1))
        velocity_r = vr(aircraft_weight_tons, velocity_1)
        app.setLabel("vr_label", '{} knots'.format(velocity_r))


#     Main startup
app = gui("Boeing 737NG V-Speed Calculator", "525x300")

app.addLabel("title", "Boeing 737NG V-Speed Calculator", 0, 0, 3)       # Row 0,Column 0,Span 2
app.setLabelFont(16, font="Times New Roman")

app.addLabel("variant", "Select 737 variant: ", 1, 0)     # Row 1, Column 0
app.setLabelAlign("variant", "left")

app.addRadioButton("airplane_variant", "Boeing 737-700", 1, 1)
app.addRadioButton("airplane_variant", "Boeing 737-800", 2, 1)

app.addLabel("weight_label", "Enter takeoff weight in pounds:", 3, 0)
app.setLabelAlign("weight_label", "left")

app.addNumericEntry("weight", 3, 1)

app.addLabel("v1_text", "V1 =       ", 4, 0)
app.setLabelAlign("v1_text", 'center')
app.addLabel("v1_label", "", 4, 1)

app.addLabel("vr_text", "VR =       ", 5, 0)
app.setLabelAlign("vr_text", "center")
app.addLabel("vr_label", "", 5, 1)

app.addLabel("v2_text", "V2 =       ", 6, 0)
app.setLabelAlign("v2_text", 'center')
app.addLabel("v2_label", "", 6, 1)


app.addButtons(["Submit", "Cancel"], press, 7, 0, 2)        # Row 3,Column 0,Span 2


# app.setEntryFocus("indicated")
app.go()
