#crown detection program

import cv2 as cv
import numpy as np
import math

#image being analyzed and threshold
imagenr = 1
threshold = 0.65

#import crown templates in all orientations
temp0 = cv.imread("dataset/Crown_Template.png", 0)
temp90 = cv.imread('dataset/Crown_Template90.png',0)
temp180 = cv.imread('dataset/Crown_Template180.png',0)
temp270 = cv.imread('dataset/Crown_Template270.png',0)

#store width and height of template in w and h, in both 0 and 90 orientation
w0, h0 = temp0.shape[::-1]
w90, h90 = temp90.shape[::-1]

#import board with imagenr
board = cv.imread('dataset/Cropped and perspective corrected boards/' + str(imagenr) + '.jpg')

#convert input board to greyscale
board_gray = cv.cvtColor(board, cv.COLOR_BGR2GRAY)

#template matching with each rotation of the crown mask
res0 = cv.matchTemplate(board_gray,temp0,cv.TM_CCOEFF_NORMED)
res90 = cv.matchTemplate(board_gray,temp90,cv.TM_CCOEFF_NORMED)
res180 = cv.matchTemplate(board_gray,temp180,cv.TM_CCOEFF_NORMED)
res270 = cv.matchTemplate(board_gray,temp270,cv.TM_CCOEFF_NORMED)

#find locations in the template matched image, where the results are over the threshhold
loc0 = np.where(res0 >= threshold)
loc90 = np.where(res90 >= threshold)
loc180 = np.where(res180 >= threshold)
loc270 = np.where(res270 >= threshold)

#empty array for storing crowns locations
crown_arr = np.zeros((5,5))

#the procedure for finding the crowns counted more than once
#crown counter to compare the current crown to the previous
crowns = 0
#go through all locations from template mathing with the upright template
for currLoc in zip(*loc0[::-1]):
    #boolean to determine whether to count a crown or not
    countThis = True
    #go through all crowns detected
    for i in range(crowns):
        #calculate distance to previous crowns
        xDist = abs(loc0[0][i] - currLoc[1])
        yDist = abs(loc0[1][i] - currLoc[0])
        #if distance to before registered crowns is less than 5, count boolean becomes false
        if(xDist < 5) and (yDist < 5):
            countThis = False
    #add one to crowns
    crowns += 1
    #if countThis is true, and crown is not a duplicate, put rectangle around and add to crown array
    if countThis:
        cv.rectangle(board, currLoc, (currLoc[0] + w0, currLoc[1] + h0), (0,0,255), 2)
        crown_arr[math.floor(currLoc[1]/100),math.floor(currLoc[0]/100)] += 1

#same procedure for 90,180,270 degree templates
#90:
crowns = 0
for currLoc in zip(*loc90[::-1]):
    countThis = True
    for i in range(crowns):
        xDist = abs(loc90[0][i] - currLoc[1])
        yDist = abs(loc90[1][i] - currLoc[0])
        if(xDist < 5) and (yDist < 5):
            countThis = False
    crowns += 1
    if countThis:
        cv.rectangle(board, currLoc, (currLoc[0] + w90, currLoc[1] + h90), (0,0,255), 2)
        crown_arr[math.floor(currLoc[1]/100),math.floor(currLoc[0]/100)] += 1
#180:
crowns = 0
for currLoc in zip(*loc180[::-1]):
    countThis = True
    for i in range(crowns):
        xDist = abs(loc180[0][i] - currLoc[1])
        yDist = abs(loc180[1][i] - currLoc[0])
        if(xDist < 5) and (yDist < 5):
            countThis = False
    crowns += 1
    if countThis:
        cv.rectangle(board, currLoc, (currLoc[0] + w0, currLoc[1] + h0), (0,0,255), 2)
        crown_arr[math.floor(currLoc[1]/100),math.floor(currLoc[0]/100)] += 1
#270:
crowns = 0
for currLoc in zip(*loc270[::-1]):
    countThis = True
    for i in range(crowns):
        xDist = abs(loc270[0][i] - currLoc[1])
        yDist = abs(loc270[1][i] - currLoc[0])
        if(xDist < 5) and (yDist < 5):
            countThis = False
    crowns += 1
    if countThis:
        cv.rectangle(board, currLoc, (currLoc[0] + w90, currLoc[1] + h90), (0,0,255), 2)
        crown_arr[math.floor(currLoc[1]/100),math.floor(currLoc[0]/100)] += 1

cv.imshow("Crown Board", board)
cv.waitKey(0)
