import cv2
import os
import shutil
import math

def createRect(point, width, height, type, xoffset, yoffset):
    xOffset = xoffset
    yOffset = yoffset

    x1 = point[0] - xoffset
    if x1<0: x1 = 0
    y1 = point[1] - yOffset
    if y1 <0: y1 = 0
    x2 = point[0] + xOffset
    if x2>width: x2 = width
    y2 = point[1] + yOffset
    if y2>height: y2 = height

    return str(int(x1))+","+str(int(y1))+","+str(int(x2))+","+str(int(y2))+","+str(type)+" "

# path = "/home/sdb2/doan/Train/"
# path = "D:/doan/business_cards/"
# des = "D:/doan/business_cards/"
# f = open("Summary.csv", "r")
# fTrain = open("TrainCardPointModifier.csv","w")
# fYolo = open("TrainCardYolo.txt","fw")

path = "D:/doan/results/"
des = "D:/doan/results/"
f = open("gen_csv.csv", "r")
fTrain = open("TrainCardPointModifier2.csv","w")
fYolo = open("TrainCardYolo2.txt","w")


## format
## name bx11,by12,bx13,by14,0 bx21,by22,bx23,by24,1 bx31,by32,bx33,by34,2 bx41,by42,bx43,by44,3
lines = f.readlines()
for line in lines:
    #print(line)
    lineArr = line.strip().split(",")
    imageName = lineArr[0]
    if os.path.exists(path + imageName):
        image = cv2.imread(path+imageName)
        xPoint1 = float(lineArr[1])
        yPoint1 = float(lineArr[2])

        xPoint2 = float(lineArr[3])
        yPoint2 = float(lineArr[4])

        xPoint3 = float(lineArr[5])
        yPoint3 = float(lineArr[6])

        xPoint4 = float(lineArr[7])
        yPoint4 = float(lineArr[8])

        height, width, _ = image.shape
        listPoint = [(xPoint1,yPoint1),(xPoint2, yPoint2),(xPoint3, yPoint3),(xPoint4,yPoint4)]
        listPointRect = [(0,0),(width, 0),(width, height),(0,height)]
        listPointNew = []
        for item in listPointRect:
            distMin = 1000000
            indexSelected = 0
            for index in range(len(listPoint)):
                point = listPoint[index]
                dist = math.sqrt(math.pow((item[0]-point[0]),2)+math.pow((item[1]-point[1]),2))
                if dist < distMin:
                    distMin = dist
                    indexSelected = index

            listPointNew.append(listPoint[indexSelected])
            listPoint.pop(indexSelected)
        fTrain.write("\n{},{},{},{},{},{},{},{},{}".format(imageName, listPointNew[0][0] , listPointNew[0][1], listPointNew[1][0], listPointNew[1][1], listPointNew[2][0], listPointNew[2][1], listPointNew[3][0],listPointNew[3][1]))
        #########
        newLine = des + imageName + " "
        count = 0
        for item in listPointNew:
            tmp=width if width<height else height
            tmp=int(tmp/20)
            newLine += createRect(item, width, height, count, tmp, tmp)
            count += 1
        print(newLine)
        fYolo.write(newLine.rstrip(" ")+"\n")
f.close()
#fTrain.close()
fYolo.close()

