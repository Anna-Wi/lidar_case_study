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

SortedAngles = Sorted[0]
SortedDistances = Sorted[1]
SortedDistancesX = Sorted[2]
SortedDistancesY = Sorted[3]

#Now I want to try and get the mean for ranges of 1 degree
MeanAngles = []
MeanDistances = []
MeanX = []
MeanY = []


for ang in range(0,360):
    
    #print(ang)
    #print(len(MeanDistances))        
    #print(MeanAngles)
    #print(MeanDistances)
    sumphi = 0
    sumrho = 0
    numberofvalues = 0
    for i in range(0,len(SortedAngles)):
       #Get the mean for an interval (length 1 degree) of points 
        if SortedAngles[i] >= ang + 1:
            #if there is just one value in the interval, I treat it as an outlier
            if numberofvalues <= 1:
                break
            else:
                #if not, I calculate the mean
                MeanAngles.append(sumphi/numberofvalues)
                MeanDistances.append(sumrho/numberofvalues)
                [X,Y] = pol2cart(sumrho/numberofvalues, -(2 * math.pi * sumphi/numberofvalues / 360))
                MeanX.append(X)
                MeanY.append(Y)
                break
        elif ang <= SortedAngles[i] < ang + 1:
            sumphi = sumphi + SortedAngles[i]
            sumrho = sumrho + SortedDistances[i]
            numberofvalues = numberofvalues + 1
        
        

#Now I want to find the corners and the areas with little/no data

Xcorners = []
Ycorners = []

Xred = []
Yred = []

#AnglesBetweenValues = []
#DistancesBetweenValues = []

Xfinal = []
Yfinal= []
Ispointblack = []



i=1
while i < len(MeanAngles)-1:
      

    Distance = MeanDistances[i]
    Distanceplus1 = MeanDistances[i+1]
    Distanceminus1 = MeanDistances[i-1]
    

    if (Distanceplus1-Distance < 0 and Distance-Distanceminus1 > 0 or 
    Distanceplus1-Distance > 0 and Distance-Distanceminus1 < 0):
    #(Distanceplus1-Distance < 0 and Distanceplus2-Distance < 0 and Distance-Distanceminus1 > 0 and Distance-Distanceminus2 > 0 or 
    #Distanceplus1-Distance > 0 and Distanceplus2-Distance > 0 and Distance-Distanceminus1 < 0 and Distance-Distanceminus2 < 0):
        Xcorners.append(MeanX[i])
        Ycorners.append(MeanY[i])
        Xfinal.append(MeanX[i])
        Yfinal.append(MeanY[i])
        Ispointblack.append(True)
    if distance(MeanX[i],MeanX[i+1],MeanY[i],MeanY[i+1]) > 450:
        Xred.append(MeanX[i])
        Xred.append(MeanX[i+1])
        Yred.append(MeanY[i])
        Yred.append(MeanY[i+1])
        Xfinal.append(MeanX[i])
        Yfinal.append(MeanY[i])
        Ispointblack.append(False)
        Xfinal.append(MeanX[i+1])
        Yfinal.append(MeanY[i+1])
        Ispointblack.append(False)
    i=i+1

Xfinal.append(Xfinal[0])
Yfinal.append(Yfinal[0])
Ispointblack.append(Ispointblack[0])

"""
i = 1
while i < len(MeanX)-1:
    Xvalue = MeanX[i]
    Yvalue = MeanY[i]

    Xvalue2 = MeanX[i+1]
    Yvalue2 = MeanY[i+1]
    
    Xvalue3 = MeanX[i-1]
    Yvalue3 = MeanY[i-1] 

    AnglesBetweenValues.append(getAngle(Xvalue,Yvalue,Xvalue2,Yvalue2,Xvalue3,Yvalue3))
    DistancesBetweenValues.append(distance(Xvalue,Xvalue2,Yvalue,Yvalue2))
    if distance(Xvalue,Xvalue2,Yvalue,Yvalue2) < 400: #first value: 2000
        #only when ecke the point will be saved for the plot later on
        #first_try_figure1: for angles > 40 and < 140
        print(getAngle(Xvalue,Yvalue,Xvalue2,Yvalue2,Xvalue3,Yvalue3))
        if (getAngle(Xvalue,Yvalue,Xvalue2,Yvalue2,Xvalue3,Yvalue3) > 30 and getAngle(Xvalue,Yvalue,Xvalue2,Yvalue2,Xvalue3,Yvalue3) < 150
        or getAngle(Xvalue,Yvalue,Xvalue2,Yvalue2,Xvalue3,Yvalue3) > 210 and getAngle(Xvalue,Yvalue,Xvalue2,Yvalue2,Xvalue3,Yvalue3) < 330):
            Xcorners.append(Xvalue)
            Ycorners.append(Yvalue)
    else:
        Xred.append(Xvalue)
        Xred.append(Xvalue2)
        Yred.append(Yvalue)
        Yred.append(Yvalue2)
    i=i+1
"""

with open("results.txt", "w") as file:
    file.write("#Xvalue Yvalue Black?(if red = False)\n")
    for row in range(len(Xfinal)):

        file.write(str(Xfinal[row]))
        file.write(" ")
        file.write(str(Yfinal[row]))
        file.write(" ")
        file.write(str(Ispointblack[row]))
        file.write("\n")

#plt.scatter(MeanX,MeanY,color="gray", marker = ".")
#plt.scatter(Xcorners, Ycorners ,color="blue", marker = ".")
#plt.scatter(Xred, Yred, color="red", marker=".")
plt.plot(Xfinal,Yfinal,color="black")
#plotting red lines:
k=0
while k < len(Xred):
    plt.plot([Xred[k],Xred[k+1]],[Yred[k],Yred[k+1]],color="red")
    k=k+2
plt.axis("scaled")
#hiding the x and y axis
ax = plt.gca()

#hide x-axis
ax.get_xaxis().set_visible(False)

#hide y-axis
ax.get_yaxis().set_visible(False)
#plt.show()
plt.savefig("Final_result.png")
#print(len(Xcorners))
