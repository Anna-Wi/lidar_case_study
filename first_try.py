from PlotLidarData import cart2pol, pol2cart
import numpy as np
import csv
import math
import matplotlib.pyplot as plt

#determine the distance between two points with coordinates (x1,y1) and (x2,y2)
def distance(x1,x2,y1,y2):
    return np.sqrt((x2-x1)**2+(y2-y1)**2)

#determine the angle between three points a, b and c with coordinates (a1,a2), (b1,b2) and (c1,c2)
def getAngle(a1, a2, b1, b2, c1, c2):
    ang = math.degrees(math.atan2(c2-b2, c1-b1) - math.atan2(a2-b2, a1-b1))
    return ang + 360 if ang < 0 else ang


with open('out_startplatz_cut.txt') as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\t')
    NewRotations = []
    MeasurementQualities = []
    MeasurementAngles = []
    MeasurementDistances = []
    MeasurementDistancesX = []
    MeasurementDistancesY = []

    #new arrays for sorting of values
    MeasurementAngles2 = []
    MeasurementDistances2 = []
    
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

            MeasurementAngles2.append(MeasurementAngle)
            MeasurementDistances2.append(MeasurementDistance)
            
        else:
            MeasurementDistance = None

        # [MeasurementDistanceX, MeasurementDistanceY] = pol2cart(MeasurementDistance, (2*math.pi*MeasurementAngle/360))

        NewRotations.append(NewRotation)
        MeasurementQualities.append(MeasurementQuality)
        MeasurementAngles.append(MeasurementAngle)
        MeasurementDistances.append(MeasurementDistance)

#print(len(MeasurementDistances2))
#print(len(MeasurementAngles2))
#print(len(MeasurementDistancesX))

#I combine the lists to sort them by ascending angle values
Tobesorted = np.array([MeasurementAngles2,MeasurementDistances2,MeasurementDistancesX,MeasurementDistancesY])

#define new matrix with columns sorted in ascending order by angle values in first row
Sorted = Tobesorted[:, np.argsort(Tobesorted[0, :])]

#Now I go back to lists to look at the distances of neighbouring values
SortedDistancesX = Sorted[2]
SortedDistancesY = Sorted[3]


#initializing of lists for the values

DistanceBetweenValues = []
AnglesBetweenValues = []
#here I include the first (random) data point to have a connected plot later on
XforPlots = [SortedDistancesX[0]]
YforPlots = [SortedDistancesY[0]]

Xred = []
Yred= []

#determine distance and angles between neighbouring values
i = 1
while i < len(SortedDistancesX)-1:
    Xvalue = SortedDistancesX[i]
    Yvalue = SortedDistancesY[i]

    Xvalue2 = SortedDistancesX[i+1]
    Yvalue2 = SortedDistancesY[i+1]
    
    Xvalue3 = SortedDistancesX[i-1]
    Yvalue3 = SortedDistancesY[i-1] 

    AnglesBetweenValues.append(getAngle(Xvalue,Yvalue,Xvalue2,Yvalue2,Xvalue3,Yvalue3))
    DistanceBetweenValues.append(distance(Xvalue,Xvalue2,Yvalue,Yvalue2))

    if distance(Xvalue,Xvalue2,Yvalue,Yvalue2) < 300: #first value: 2000
        #only when the angle has a certain value, they are saved to (hopefully) mark corner points
        #first_try_figure1.png: for angles > 40 and < 140
        if getAngle(Xvalue,Yvalue,Xvalue2,Yvalue2,Xvalue3,Yvalue3) > 40 and getAngle(Xvalue,Yvalue,Xvalue2,Yvalue2,Xvalue3,Yvalue3) < 140:
            XforPlots.append(Xvalue)
            YforPlots.append(Yvalue)
    #if the distance between neighbouring values is higher than as defined above (here: 300),
    #they are saved to later be marked as red
    else:
        Xred.append(Xvalue)
        Xred.append(Xvalue2)
        Yred.append(Yvalue)
        Yred.append(Yvalue2)

       
    #later on i could round some values?
    #tried i = i+3, not great
    i=i+1

#print(min(DistanceBetweenValues))
#print(max(DistanceBetweenValues))
#print(DistanceBetweenValues[0:20])
#print(AnglesBetweenValues[0:20])

plt.plot(XforPlots,YforPlots, color="black",marker="x")
plt.scatter(Xred,Yred,color="red")
plt.axis("scaled")
#plt.plot(Xred,Yred, color="red")
plt.show()

#print(len(XforPlots))
#print(len(SortedDistancesX))




