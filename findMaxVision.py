#!/home/pi/Desktop/launcher.sh python
# import the necessary packages

from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import signal
import cv2
import numpy as np
from piVideoStream329v1 import PiVideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import datetime
import math
from math import e
from networktables import NetworkTables as nt
import sys
import os
import select
import socket

count = 1
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(0)
print('Network Tables is setup on Pi')

while 1:
    try:
       ip = socket.gethostbyname('329.local')
       print('Connected to robot')
       break
    except:
        print('Waiting for NWT and Roborio connection')
        time.sleep(.5)
        pass
nt.initialize(server=ip)
sd = nt.getTable("SmartDashboard")

def findMax(coords):
    Max = 480.0
    idx = 0
    if len(coords) > 0:
        x = 0
        for c,i in enumerate(coords):
            if int(coords[x])<Max:
                Max=coords[x]
                
                
                idx = x
            x = x + 1
    else:
        return Max,idx
    return Max,idx
    
def contour(cts):
    rect = cv2.minAreaRect(cts)
    box = cv2.boxPoints(rect)
    return(np.int0(box),rect)
    


def CalcProperties(x):
   # dist = (0.002 * x ** (2))+(0.083*x)+90.216
    #dist = (0.00017*(x**2))-(0.0492*x)+71.482
    dist = 59.557*(e**(0.0041*x))
    return(dist)

def angleProperties(pixCount):
    theta = 0.09375 * pixCount
    return theta

vs = PiVideoStream().start() # Start taking frames

display= vs.read()

coordList = []
boxList = []

d = 0

turnA = ''
rightSide = False
leftSide = False
inCenter = False

arb = 10000
ars = 15 
while True:
    count += 1
    turnangle = 999
    try:
        r = piAlive(r)
    except:
        pass

    if count > 200: #Only check network connection every 200 Frames
       count = 0
       start_time = time.time()
       try:
           while True:
               ip = socket.gethostbyname('roboRIO-329-FRC.local')
               nt.initialize(server=ip)
               sd = nt.getTable("SmartDashboard")
               #print("Network reconnected")
               break                
       except Exception as ex:
               print(ex)
               turnAng = 999
               time.sleep(1)
               pass
    if True:
        found = False
        process = True
        frame = vs.read() # read the most recent frame
        if np.array_equal(frame,display) == True: #Checks if this is a unique frame
            Duplicate = True
        else:
            display=frame #set the new frame to display so it can check if the next is new

            low=np.array([50,180,125])
            high=np.array([70 ,255,255])
            #low=np.array([81,121,249])
            #high=np.array([84 ,147,255])
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #Change image to HSV
            mask = cv2.inRange(hsv, low, high) #Apply Mask to image so only targets are white all else is black
            ct = None
            
            
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # Find the contours of the mask
            cnts = list(cnts)
            if len(cnts)!=0:  #only runs the following if you see something
                zzzzzz = 4
                coordList = []
                xCoordList = []
                boxList = []
                pixCount = 0
                too_small = []
                ct = 0
                
                for cts in cnts:
                    ### Find boundries and draw rectangle on image
                    
                    
                    
                    boxd,rect = contour(cts)#### Creates box form contours
                    area1 = list(rect)
                    cv2.drawContours(display,[boxd.astype(int)],0,(0,0,255),2)
                    
                    area = area1[1][0]*area1[1][1]
                    
                    if area < ars or area > arb:
                        #print('Found small area')
                        too_small.append(ct)
                    ct +=1
                    
                    heightList = list(rect)
                    height = heightList[0][1] - (heightList[1][1]/2)
                    xLocation = heightList[0][0]
                    coordList.append(height)
                    xCoordList.append(xLocation)
                    boxList.append(boxd.astype(int))
                if ct is not None and len(boxList)>0:
                    for c in range(1, len(too_small) + 1):#Get Rid of too small edit to get rid of too big too if you need it
                        del coordList[too_small[-c]]
                        del boxList[too_small[-c]]
                        del cnts[too_small[-c]]
                        del xCoordList[too_small[-c]]
                    
                   # print(boxList[idx])
                    
                 #   print(coordList)
                   # print(boxList)
                    if len(boxList)>0:
                        Max,idx = findMax(coordList)
                        pixCount2 = xCoordList[idx] 
                        pixCount = 320-xCoordList[idx] 
                        d = CalcProperties(Max)
                        theta = angleProperties(pixCount)
                        cv2.drawContours(display,[boxList[idx]],0,(255,255,255),2)
                        if xCoordList[idx] >= 315 and xCoordList[idx] <= 325:
                            inCenter = True
                            ightSide = False
                            leftSide = False;
                        elif xCoordList[idx] > 325:
                            rightSide = True
                            inCenter = False
                            leftSide = False
                        elif xCoordList[idx] < 315:
                            leftSide = True
                            inCenter = False
                            rightSide = False#Draws box on image these are the red boxes.  Its what you see
                    else:
                        d = 0
                        theta = 0
                        pixCount = 0
                else:
                    Max,idx = findMax(coordList)
                    d = 0
                    pixCount = 0
                    theta = 0
            Max,idx = findMax(coordList)
            if leftSide == True:
                turnA = 'Left'
            elif rightSide == True:
                turnA = 'Right'
            elif inCenter == True:
                turnA = 'In Center'
            else:
                turnA = 'Could not get turn'
            if Max != 0 and d != 0:
               # screenText = 'Height=' + str(round(Max,1))
                screenText = 'Dist=' + str(round(d,1)) + ' Turn: '+str(round(theta,1)) + ' Pixcount: '+str(round(pixCount2,1))
                #cv2.line(display,(320,10),(320,470),(255,0,0),2) #draw line in middle of screen
                font                   = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10,300)
                fontScale              = 1
                fontColor              = (255,255,255)
                lineType               = 2
                cv2.putText(display, screenText, 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)### Put text on the screen

             try:
                    sd.putNumber("Turn Angle", theta) #Add these back in to send data to Network tables
                    sd.putString("Turn ", turnA)
                    sd.putNumber('Distance Away',d)
             except:
                    pass
            #cv2.imshow("Mask", mask) ##look at mask image  ############ COMMENT OUT WHEN ON ROBOT !!!!!!!!!!!!!!!!!! Huge speed penalty
            #cv2.imshow("Frame",display) ## look at what it sees ############ COMMENT OUT WHEN ON ROBOT !!!!!!!!!!!!!!!!!!

            
            #Comment back in to see time per frame
            #print('time', time.time() - currentTime)

            key = cv2.waitKey(1) & 0xFF


    else:
        vs.stop()
        #print('Stopping')
        #os.system("sudo shutdown -h now")  ### you can use this to shutdown.  But you should use a battery pack


# do a bit of cleanup
cv2.destroyAllWindows()
vs329.PiVideoStream.stop()
