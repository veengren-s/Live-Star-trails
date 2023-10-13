import os
import cv2
from PIL import Image, ImageTk
import time
import tkinter as tk
from tkinter import filedialog
from LiveTrails import *

root = tk.Tk()
prevStacked = False
runB = False
file = ''
read = []
tempImg = []
width = root.winfo_screenwidth()               
height = root.winfo_screenheight()
cwidth = width-300
cheight = height
startB,stopB = '',''


iwidth=0
iheight=0 
root.geometry("%dx%d" % (width, height))      
canvas = tk.Canvas(root, width=cwidth, height=cheight, bg='skyblue')



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
            print(filePath)
            image = cv2.imread(filePath + "\\" + files)
            imageArray.append(image)

    return imageArray

def lighten(images):
    global iwidth,iheight
    #create grayscale copy
    result = images[0]
    imageGray = []
    for image in images:
        imageGray.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    iwidth, iheight = images[0].shape[:2]
    i = 0

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
    global tempImg
    fileList = scan(filePath)
    fileList = cullFileList(fileList, read)
    images = load(fileList,filePath)
    results = lighten(images)
    tempImg = results
    cv2.imwrite(filePath + "\\temp.jpg", results)
    return results

#checks for new files
def check(filePath, read):
    currentFiles = scan(filePath)
    print(file)
    print(read)
    print(currentFiles)

    #we have a new file
    if currentFiles != read:
        print("new files")
        stack(filePath, read)
        read = currentFiles
    else:
        print("No new files")
    return read

def run():
    global read, runB
    if runB:
        read = check(file, read)
    root.after(50000, run)
    
def fileExplorer():
    global file
    file = tk.filedialog.askdirectory()
    if file != '':
        startB['state']="normal"
        

def start():
    global tempImg, runB, file
    runB = True
    startB['state']="disabled"
    stopB['state']="normal"
    run()
    print("beep")
    sWidth = cwidth
    sHeight = round(cwidth/iheight*iwidth)
    tempImg = ImageTk.PhotoImage(Image.open(file+"\\temp.jpg").resize((sWidth,sHeight), Image.ANTIALIAS))
    canvas.create_image(0,0, anchor="nw", image=tempImg)

def stop():
    global runB
    runB = False
    startB['state']="normal"
    stopB['state']="disabled"

  
controls = tk.Frame(root)
#Folder selection:
tk.Label(controls, text= "Select Folder to Monitor: ").pack(anchor='nw')
button = tk.Button(controls, text="select folder", command=fileExplorer).pack(anchor='nw')

#Star/Stop monitoring
startB = tk.Button(controls, text="START", command=start)
startB.pack(anchor='nw')

stopB = tk.Button(controls, text="STOP", command=stop)
stopB.pack(anchor='nw')
controls.pack(side="left", anchor="nw")

#image
canvas.pack()

tk.Label(root, image=tempImg).pack()

# console
console = tk.Frame(root)
tk.Label(console, text="CONSOLE: ").pack(side="right")

console.pack(side="right")
#disable buttons
stopB["state"] = 'disabled'
startB["state"] = 'disabled'

root.after(5000, run)
root.mainloop()

#USE AFTER FOR LOOPING FUCTION