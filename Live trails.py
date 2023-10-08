import os
import cv2
import time
WIDTH = 0
HEIGHT = 0
prevStacked = False

# Scans the selected folder and returns an array with all the files
def scan(filePath):
    files = os.listdir(filePath)
    return files

def load(fileList, filePath):
    imageArray = []
    for files in fileList:
        length = len(files)
        end = files[length-3:length]

        if end == "jpg":
            image = cv2.imread(filePath + "\\" + files)
            imageArray.append(image)

    return imageArray

def lighten(images):
    #create grayscale copy
    result = images[0]
    imageGray = []
    for image in images:
        imageGray.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    width, height = images[0].shape[:2]

    for x in range(0,width):
        for y in range(0,height):
            max = 0
            for i in range(0,len(images)):
                if imageGray[i][x][y] > imageGray[max][x][y]:
                    max = i
            result[x][y][0] = images[max][x][y][0]
            result[x][y][1] = images[max][x][y][1]
            result[x][y][2] = images[max][x][y][2]
    return result
        
#removes already stacked files and any other unwanted stuff
def cullFileList(fileList,read):
    culledList = []
    for img in fileList:
        if img not in read:
            culledList.append(img)
    
    if "temp.jpg" in fileList:
        culledList.append("temp.jpg")
    return culledList
    
#Runs the stacking,scanning and reading steps
def stack(filePath, read):
    fileList = scan(filePath)
    fileList = cullFileList(fileList, read)
    images = load(fileList,filePath)
    results = lighten(images)
    cv2.imwrite(filePath+ "\\temp.jpg", results)
    return results
    prevStacked = True

#checks for new files
def check(filePath, read):
    currentFiles = scan(filePath)

    #we have a new file
    if currentFiles != read:
        print("new files")
        stack(filePath, read)
        read = currentFiles
    else:
        print("No new files")
    return read

read = []
i = 0
while(i < 20):
    print(i)
    res = check("Live-Star-trails\\test", read)
    read = res
    time.sleep(5)
    i += 1