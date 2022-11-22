#crown detection program

import cv2 as cv
import numpy as np
import math

#image being analyzed and threshold
imagenr = 30
threshold = 0.65

#import crown templates in all orientations
temp0 = cv.imread("dataset/Crown_Template.png", 0)
temp90 = cv.imread('dataset/Crown_Template90.png',0)
temp180 = cv.imread('dataset/Crown_Template180.png',0)
temp270 = cv.imread('dataset/Crown_Template270.png',0)

#store width and height of template in w and h
w, h = temp0.shape[::-1]

#import board
board = cv.imread('dataset/Cropped and perspective corrected boards/' + str(imagenr) + '.jpg')

#convert input board greyscale
board_gray = cv.cvtColor(board, cv.COLOR_BGR2GRAY)

#empty array for storing crowns locations
crown_arr = np.zeros((5,5))

#template matching with each orientation of the crown mask
res0 = cv.matchTemplate(board_gray,temp0,cv.TM_CCOEFF_NORMED)
res90 = cv.matchTemplate(board_gray,temp90,cv.TM_CCOEFF_NORMED)
res180 = cv.matchTemplate(board_gray,temp180,cv.TM_CCOEFF_NORMED)
res270 = cv.matchTemplate(board_gray,temp270,cv.TM_CCOEFF_NORMED)

#find where in the template matched image, the match is over the threshhold
loc0 = np.where( res0 >= threshold)
loc0 = np.where(res0 >= threshold)
loc90 = np.where(res90 >= threshold)
loc180 = np.where(res180 >= threshold)
loc270 = np.where(res270 >= threshold)

#variable used in order to identify duplicate crowns
crownCounter = 0

#go through all locations found in the template matching
for pt in zip(*loc0[::-1]):
    #boolean value, used in deciding wheter to count a crown, starts as true
    countThis = True
    #go through all the crowns counted so far
    for i in range(crownCounter):
        #calculate the distance to a given crown in x and y
        xDist = abs(loc0[0][i] - pt[1])
        yDist = abs(loc0[1][i] - pt[0])
        #if the crown is too close, don't count it
        if (abs(loc0[0][i] - pt[1]) < 5) and (abs(loc0[1][i] - pt[0]) < 5):
            countThis = False
    #add one to crown counter
    crownCounter += 1
    #if the crown is not found to be a duplicate, add it to the crowns array
    if countThis:
        cv.rectangle(board, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        crown_arr[math.floor(pt[1]/100),math.floor(pt[0]/100)] += 1

#the same procedure is used for the 90, 180 and 270 degree templates
crownCounter = 0
loc90 = np.where( res90 >= threshold)
for pt in zip(*loc90[::-1]):
    countThis = True
    for i in range(crownCounter):
        if (abs(loc90[0][i] - pt[1]) < 5) and (abs(loc90[1][i] - pt[0]) < 5):
            countThis = False
    crownCounter += 1
    if countThis:
        cv.rectangle(board, pt, (pt[0] + h, pt[1] + w), (0,0,255), 2)
        crown_arr[math.floor(pt[1]/100),math.floor(pt[0]/100)] += 1

crownCounter = 0
loc180 = np.where( res180 >= threshold)
for pt in zip(*loc180[::-1]):
    countThis = True
    for i in range(crownCounter):
        if (abs(loc180[0][i] - pt[1]) < 5) and (abs(loc180[1][i] - pt[0]) < 5):
            countThis = False
    crownCounter += 1
    if countThis:
        cv.rectangle(board, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        crown_arr[math.floor(pt[1]/100),math.floor(pt[0]/100)] += 1

crownCounter = 0
loc270 = np.where( res270 >= threshold)
for pt in zip(*loc270[::-1]):
    countThis = True
    for i in range(crownCounter):
        if (abs(loc270[0][i] - pt[1]) < 5) and (abs(loc270[1][i] - pt[0]) < 5):
            countThis = False
    crownCounter += 1
    if countThis:
        cv.rectangle(board, pt, (pt[0] + h, pt[1] + w), (0,0,255), 2)
        crown_arr[math.floor(pt[1]/100),math.floor(pt[0]/100)] += 1

#all crown locations are combined into a singe array.
crownLoc = [loc0[:], loc90[:], loc180[:], loc270[:]]

#prints out the final crowns
print("Crowns:")
print(crown_arr[:])

cv.imshow("Crown Board", board)
cv.waitKey(0)