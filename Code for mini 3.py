import cv2 as cv
import numpy as np

#Tiles with and without crowns average BGR Values, Found manually.
#Yellow crown: [77, 144, 146] Green crown: [99, 128, 122] Blue crown: [102, 110, 102], Pink crown [98, 119, 129]
#Forest: [19, 41, 33] Forest with crown: [28, 67, 61]
#Grass: [25, 143, 97] Grass with crown: [21, 120, 101] Grass with two crowns: [35, 118, 112]
#Corn: [7, 167, 190] Corn with crown: [14, 136, 160]
#Ocean: [159, 91, 16] Ocean with crown: [122, 91, 55]
#Mine: [27, 47, 54] Mine with crown: [25, 38, 44] Mine with two crowns: [21, 49, 59] Mine with three crowns: [31, 62, 74]
#Wasteland: [48, 85, 96] Wasteland with crown: [54, 94, 106] Wasteland with two crowns: [56, 97, 111]


#Different BGR values of each type of tile, BGR not RGB since openCV reads the RGB colors as BGR. These are the average values from the data above
crownTile = [94, 125, 124]
forestTile = [23, 54, 45] 
grassTile = [27, 127, 103]
cornTile = [10, 151, 175]
oceanTile = [140, 91, 35]
mineTile = [26, 49, 61] 
wastelandTile = [53, 92, 104] 

#array of tiles average values, used to determin tiles
tileArray = [crownTile, forestTile, grassTile, cornTile, oceanTile, mineTile, wastelandTile]
#Array of the names, for visualising the guess of the tiles later on
nameArray = ["Crown", "Forest", "Grass", "Corn", "Ocean", "Mine", "Wasteland"]

### Reading the specific image we want to know the score of ###
#Board number, change if different board is wanted (from 1 to 74)
boardnr = 2

board = cv.imread('King Domino dataset/King Domino dataset/Cropped and perspective corrected boards/' + str(boardnr) + '.jpg')

###############################################################
#To use the BGR values of each tile, the board needs to be divided into 25 tiles. A way to do this is to make the board 5x5 pixels,
#and get the average color of each tile from the main image placed in the 5x5
#The lenght would then be 5 pixels
boardLenght = 5
#An image is then made with 5x5 black pixels
blank = np.zeros((boardLenght,boardLenght,3), dtype='uint8')

#Array keeping the guesses 
guessArray = np.zeros((boardLenght,boardLenght), dtype='U16')

#Array keeping the Index
indexArray = np.zeros((boardLenght,boardLenght), dtype='uint8')

#Array keeping the color distance from each tile
distanceArray = np.zeros((boardLenght,boardLenght), dtype='uint8')

for row in range(boardLenght): #boardLenght is used because there will be 5 tiles pr. row and pr. column
    for column in range(boardLenght):
        #Each tile is 100x100 pixels on the main image, because its an 500x500 image
        tileDivider = board[row*100:(row+1)*100, column*100:(column+1)*100]
        #Now we have to split the BGR colors and find the average of them for the tile in the current loop
        b,g,r = cv.split(tileDivider) 
        b = np.average(tileDivider[:, :, 0])
        g = np.average(tileDivider[:, :, 1])
        r = np.average(tileDivider[:, :, 2])
        #Now placing the aveage BGR color into the tiles in blank
        blank[row, column] = (b,g,r) #row and column is used to only change BGR for the current tile
        #Now the identification of the tiles needs to be done, this can be done by "guessing"
        #Variables used for the guessing loop further down, minDistance is the minimum distance in color for each tile
        minDistance = 500
        minIndex = 0
        #For loop looking at all tiles and what finding the smallest distance to each color for them
        for i in range(7):
            distance = np.linalg.norm(tileArray[i] - blank[row,column])
            if distance < minDistance:
                minDistance = distance
                minIndex = i
        distanceArray[row,column] = minDistance
        indexArray[row,column] = minIndex
        guessArray[row,column] = nameArray[minIndex]

##############################################################################
#Now its time to find which tiles are in a group together, for calculating the point. 
#groupnumber for naming the different groups found
groupnr = 1
#Array keeping all the groups found
allGroups = np.zeros((7, boardLenght, boardLenght))
#
#currentGroup = np.zeros((boardLenght, boardLenght))
print(allGroups)
#Starting with going through all seven different tiles, in all 25 tiles spaces
for tile in range(7):
    for row in range(boardLenght):
        for column in range(boardLenght):
            #Some variables for the tiles above and left of the current tile in the loop
            tileAbove = 0
            tileLeft = 0
            #Checking if current tile is part of the current type of tile being checked
            if guessArray[row, column] == nameArray[tile]:
                #If the row is not 0 meaning it is not the tiles all the way to the left
                if row != 0:
                    tileAbove = allGroups[tile, row-1, column]
                #If the column is not 0 meaning it is not the tiles in the top row
                if column != 0: 
                    tileLeft = allGroups[tile, row, column-1]
                #If the tileabove is different from 0 and is the current tile type, set current tile to the same number
                if tileAbove != 0:
                    allGroups[tile, row, column] = tileAbove
                #else if the tileleft is different from 0 and is the current tile type, set current tile to the same number
                elif tileLeft != 0:
                    allGroups[tile, row, column] = tileLeft
                #Else set the current tile to the current groupnr, starting with 1
                else:
                    allGroups[tile, row, column] = groupnr
                    #Then set the group number to plus 1, for the next found correct tile type.
                    groupnr = groupnr + 1
                #If tileabove and tileleft is not 0 and tileabove is not tileleft, Check the allgroupsarray, if the tile above is equal to
                #The current tileabove, set the current tile in allgroupsarray to the tile left
                if (tileAbove and tileLeft != 0) and (tileAbove != tileLeft):
                    for i in range(boardLenght):
                        for j in range(boardLenght):
                            if allGroups[tile, i , j] == tileAbove:
                                allGroups[tile, i , j] = tileLeft
    print(nameArray[tile])
    print(allGroups[tile])

#Loop for adding the groups into one array
for tile in range(7):
    groupnr += allGroups[tile]




#resizing blank to get the same size as the original picture and also giving space to write the tiles guessed
blank = cv.resize(blank, (500,500), interpolation=cv.INTER_NEAREST)

#A for loop for writing the guessed tile name in each tile. 
for row in range(boardLenght):
    for column in range(boardLenght):
        cv.putText(blank, str(nameArray[indexArray[row,column]]), (column*100+5, row*100+60), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0), 2)
      

cv.imshow('Original board', board)
cv.imshow('Guess', blank)
cv.waitKey(0)