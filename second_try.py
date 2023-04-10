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

#define new matrix with columns sorted in ascending order by values in first row
Sorted = Tobesorted[:, np.argsort(Tobesorted[0, :])]

#view sorted matrix
#Now I go back to lists to look at the distances of neighbouring values

SortedAngles = Sorted[0]
SortedDistances = Sorted[1]
SortedDistancesX = Sorted[2]
SortedDistancesY = Sorted[3]



print(MeasurementAngles2[0:30])
print(MeasurementDistances2[0:30])

Xcorners = []
Ycorners = []

XcornersSorted = []
YcornersSorted = []

Xred = []
Yred = []

i=2

while i < len(MeasurementAngles2)-2:
#Assumption here: i want to take several values to minimize errors
#I assume now that I have at least 2 values for each wall (excluding the corner)
    Angle = MeasurementAngles2[i]
    Angleplus1 = MeasurementAngles2[i+1]
    Angleplus2 = MeasurementAngles2[i+2]
    

    Distance = MeasurementDistances2[i]
    Distanceplus1 = MeasurementDistances2[i+1]
    Distanceplus2 = MeasurementDistances2[i+2]
    Distanceminus1 = MeasurementDistances2[i-1]
    Distanceminus2 = MeasurementDistances2[i-2]

    if (Distanceplus1-Distance < 0 and Distanceplus2-Distance < 0 and Distance-Distanceminus1 > 0 and Distance-Distanceminus2 > 0 or 
    Distanceplus1-Distance > 0 and Distanceplus2-Distance > 0 and Distance-Distanceminus1 < 0 and Distance-Distanceminus2 < 0):
        Xcorners.append(MeasurementDistancesX[i])
        Ycorners.append(MeasurementDistancesY[i])
        if distance(MeasurementDistancesX[i],MeasurementDistancesX[i+1],MeasurementDistancesY[i],MeasurementDistancesY[i+1]) > 500:
            Xred.append(MeasurementDistancesX[i])
            Xred.append(MeasurementDistancesX[i+1])
            Yred.append(MeasurementDistancesY[i])
            Yred.append(MeasurementDistancesY[i+1])

    i=i+1

j=2

while j < len(SortedAngles)-2:
#Assumption here: i want to take several values to minimize errors
#I assume now that I have at least 2 values for each wall (excluding the corner)
    Angle = SortedAngles[j]
    Angleplus1 = SortedAngles[j+1]
    Angleplus2 = SortedAngles[j+2]
    

    Distance = SortedDistances[j]
    Distanceplus1 = SortedDistances[j+1]
    Distanceplus2 = SortedDistances[j+2]
    Distanceminus1 = SortedDistances[j-1]
    Distanceminus2 = SortedDistances[j-2]

    if (Distanceplus1-Distance < 0 and Distanceplus2-Distance < 0 and Distance-Distanceminus1 > 0 and Distance-Distanceminus2 > 0 or 
    Distanceplus1-Distance > 0 and Distanceplus2-Distance > 0 and Distance-Distanceminus1 < 0 and Distance-Distanceminus2 < 0):
        XcornersSorted.append(MeasurementDistancesX[j])
        YcornersSorted.append(MeasurementDistancesY[j])

    j=j+1

finalCornersX = []
finalCornersY = []
#plt.scatter(MeasurementDistancesX, MeasurementDistancesY, color="black")
#plt.scatter(XcornersSorted,YcornersSorted, color="blue")
plt.plot(Xcorners,Ycorners, color="black")
plt.scatter(Xcorners,Ycorners,color="blue")
plt.scatter(Xred,Yred,color="red")

plt.axis("scaled")

plt.show()
#print(len(Xcorners))











