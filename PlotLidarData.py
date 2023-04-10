# import plotly.express as px
#
# wind = px.data.wind()
# fig = px.scatter_polar(wind, r="frequency", theta="direction")
# fig.show()
import csv

import math
import numpy as np
import plotly.graph_objects as go


def cart2pol(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return rho, phi


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)


with open('out_startplatz_cut.txt') as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\t')
    NewRotations = []
    MeasurementQualities = []
    MeasurementAngles = []
    MeasurementDistances = []
    MeasurementDistancesX = []
    MeasurementDistancesY = []
    for row in readCSV:
        NewRotation = bool(row[0])
        MeasurementQuality = float(row[1])
        MeasurementAngle = float(row[2])
        if MeasurementQuality > 10 and float(row[3]) < 5000 and float(row[3]) > 500:
            MeasurementDistance = float(row[3])
            [MeasurementDistanceX, MeasurementDistanceY] = pol2cart(MeasurementDistance,
                                                                    -(2 * math.pi * MeasurementAngle / 360))
            MeasurementDistancesX.append(MeasurementDistanceX)
            MeasurementDistancesY.append(MeasurementDistanceY)
        else:
            MeasurementDistance = None
        # [MeasurementDistanceX, MeasurementDistanceY] = pol2cart(MeasurementDistance, (2*math.pi*MeasurementAngle/360))

        NewRotations.append(NewRotation)
        MeasurementQualities.append(MeasurementQuality)
        MeasurementAngles.append(MeasurementAngle)
        MeasurementDistances.append(MeasurementDistance)
    # print(dates)
    # print(colors)
    #
    # # now, remember our lists?
    #
    # whatColor = input('What color do you wish to know the date of?:')
    # coldex = colors.index(whatColor)
    # theDate = dates[coldex]
    # print('The date of',whatColor,'is:',theDate)

fig = go.Figure(data=
go.Scatterpolar(
    r=MeasurementDistances,
    theta=MeasurementAngles,
    mode='markers',
))

fig.update_layout(showlegend=False)
fig.show()

fig = go.Figure(data=go.Scatter(x=MeasurementDistancesX, y=MeasurementDistancesY, mode='markers'))
fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1))
fig.show()
