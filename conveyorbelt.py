from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import cv2
import os
import tensorflow as ts
import matplotlib.pyplot as plt
from keras import layers, models
from tkinter import ttk

def CamSetup():
    global cap
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('http://192.168.43.1:8080/video')
    width, height = 300, 300 # Width of camera, #Height of Camera 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 

# global buttonClicked, startCameraV
camStart = True
buttonClicked  = False
startCameraV = True
global ImageToPredict
TotalCount = 0
BottleCount = 0
BowlCount = 0
CanCount = 0
CupCount = 0
PlateCount = 0

textVar = "Count of items\n"
textVar = textVar + "Total items: 0\n"
textVar = textVar + "Bottles: 0\n"
textVar = textVar + "Bowls: 0\n"
textVar = textVar + "Cans: 0\n"
textVar = textVar + "Cups: 0\n"
textVar = textVar + "Plates: 0\n"

# camera code

# while True:
#     ret, frame = cap.read()
#     ressizedFrame = cv2.resize(frame, (32,32))
#     # ressizedFrame = cv2.flip(ressizedFrame, 1)
    
#     cv2.imshow('frame', ressizedFrame)
    
#     if cv2.waitKey(1) == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()
def ClassifyFunc():
    thisDict = {0: "Bottle", 1: "Bowl", 2: "Can", 3: "Cup", 4: "Plate"}
    # convModel = legacy_load_model("ConvBeltConvNetTF")
    convModel = models.load_model("ConvBeltCNNTenFlow.keras")
    predictions = convModel.predict(ImageToPredict)
    # print(predictions)
    y_classes = predictions.argmax(axis=-1)
    # print(y_classes)
    # print(thisDict[y_classes[0]])
    global TotalCount
    global BottleCount
    global BowlCount
    global CanCount
    global CupCount
    global PlateCount
    global TkTextVar
    if thisDict[y_classes[0]] == "Bottle":
        
        TotalCount = TotalCount + 1
        BottleCount = BottleCount + 1
    elif thisDict[y_classes[0]] == "Bowl":
        TotalCount = TotalCount + 1
        BowlCount = BowlCount + 1
    elif thisDict[y_classes[0]] == "Can":
        TotalCount = TotalCount + 1
        CanCount = CanCount + 1
    elif thisDict[y_classes[0]] == "Cup":
        TotalCount = TotalCount + 1
        CupCount = CupCount + 1
    elif thisDict[y_classes[0]] == "Plate":
        TotalCount = TotalCount + 1
        PlateCount = PlateCount + 1
    
    textVar = "Count of items\n"
    textVar = textVar + "Total items: " + str(TotalCount) + "\n"
    textVar = textVar + "Bottles: " + str(BottleCount) + "\n"
    textVar = textVar + "Bowls: " + str(BowlCount) + "\n"
    textVar = textVar + "Cans: " + str(CanCount) + "\n"
    textVar = textVar + "Cups: " + str(CupCount) + "\n"
    textVar = textVar + "Plates: " + str(PlateCount) + "\n"
    TkTextVar.set(textVar)
    
    

def Takephoto(CapImage):
    cap.release()
    cv2.destroyAllWindows()

    # Capture the latest frame and transform to image 
    captured_imageGlobal = Image.fromarray(CapImage) 
    print(captured_imageGlobal)

    # Convert captured image to photoimage 
    photo_image = ImageTk.PhotoImage(image=captured_imageGlobal) 

    # Displaying photoimage in the label 
    label_cam.photo_image = photo_image 
  
    # Configure image in the label 
    label_cam.configure(image=photo_image) 

def TakePhotobtn():
    global buttonClicked
    buttonClicked = True

def startCamera():

    global startCameraV, buttonClicked, camStart
    if camStart:
        CamSetup()
        camStart = False

    if startCameraV:
        buttonPhoto["state"] = NORMAL
        startCameraV = False
    ret, frame = cap.read()
    ressizedFrame = cv2.resize(frame, (300,300))
    ressizedFrame = cv2.flip(ressizedFrame, 1)

    #Convert image from one color space to other 
    opencv_image = cv2.cvtColor(ressizedFrame, cv2.COLOR_BGR2RGBA) 
    if buttonClicked:
        global ImageToPredict
        resFrame = cv2.resize(frame, (32,32))
        resFrame = cv2.flip(resFrame, 1)
        ImageToPredict = cv2.cvtColor(resFrame, cv2.COLOR_BGR2RGB)
        ImageToPredict = ImageToPredict / 255
        ImageToPredict = ImageToPredict.reshape(1,32,32,3)
        Takephoto(opencv_image)
        buttonClicked = False
        camStart = True
        return

    # Capture the latest frame and transform to image 
    captured_image = Image.fromarray(opencv_image) 
    
    # Convert captured image to photoimage 
    photo_image = ImageTk.PhotoImage(image=captured_image) 
    
    # Displaying photoimage in the label 
    label_cam.photo_image = photo_image 
    
    # Configure image in the label 
    label_cam.configure(image=photo_image) 
        
    # Repeat the same process after every 10 milli-second 
    label_cam.after(10, startCamera)
    

VisualWindow = Tk()
TkTextVar = StringVar()
TkTextVar.set(textVar)
VisualWindow.columnconfigure(0, weight=1)
VisualWindow.columnconfigure(1, weight=3)
VisualWindow.rowconfigure(0, weight=1)
VisualWindow.rowconfigure(1, weight=1)
VisualWindow.rowconfigure(2, weight=1)
VisualWindow.rowconfigure(3, weight=5)
VisualWindow.geometry("500x500")
VisualWindow.title("Conveyor Belt Items Distinguisher")
os.getcwd()
icon  = PhotoImage(file = 'Logo.PNG')
VisualWindow.iconphoto(True, icon)
button = ttk.Button(VisualWindow, text="Start Camera")
VisualWindow.bind('<Escape>', lambda e: VisualWindow.quit())
label_cam = ttk.Label(VisualWindow) 
label_counts = ttk.Label(VisualWindow, textvariable=TkTextVar) 
# label_cam.pack(side=RIGHT, anchor=NE) 
button.config(command=startCamera)
# button.pack(side=LEFT, anchor=NW)
buttonPhoto = ttk.Button(VisualWindow, text="Take Image")
buttonPhoto.config(command=TakePhotobtn)
buttonPhoto["state"] = DISABLED
# buttonPhoto.pack(side=LEFT, anchor=SW)
ClassifyBtn = ttk.Button(VisualWindow, text="What is this")
ClassifyBtn.config(command=ClassifyFunc)
entry = ttk.Entry(VisualWindow)


# ClassifyBtn.pack(side=LEFT,anchor=SW)
button.grid(row=0, column=0, padx= 10, pady= 10, sticky='NW')
buttonPhoto.grid(row=1, column=0, padx= 10, pady= 10, sticky='NW')
ClassifyBtn.grid(row=2, column=0, padx= 10, pady= 10, sticky='NW')
label_counts.grid(row=3, column=0, padx= 10, pady= 10, sticky='NW')
label_cam.grid(row=0, column=1, rowspan= 4)
VisualWindow.mainloop()