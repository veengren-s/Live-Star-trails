import os
import cv2
WIDTH = 0
HEIGHT = 0

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
            image = cv2.imread(filePath + "/" + files)
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
            for i in range(0,len(images)-1):
                if imageGray[i][x][y] > imageGray[max][x][y]:
                    max = i
            result[x][y][0] = images[max][x][y][0]
            result[x][y][1] = images[max][x][y][1]
            result[x][y][2] = images[max][x][y][2]
    return result
        
            
def stack(filePath):
    fileList = scan(filePath)
    images = load(fileList,"test")
    results = lighten(images)
    # cv2.imshow("results", results)
    # cv2.waitKey(0)
    cv2.imwrite("test/test.jpg", results)
stack("test")
print("done")