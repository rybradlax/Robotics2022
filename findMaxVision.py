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
import sys
import os
import select


def findMax(coords):
    Max = 0
    idx = 0
    if(len(coords) > 0):
        for c,i in enumerate(coords):
            if(coords[i]>Max):
                Max=coords[i]
                idx = i
    else:
        return Max,idx
    return Max,idx
    
def contour(cts):
    rect = cv2.minAreaRect(cts)
    box = cv2.boxPoints(rect)
    return(np.int0(box),rect)
    
vs = PiVideoStream().start() # Start taking frames

display= vs.read()

coordList = []
boxList = []
while True:
    
    if True:
        found = False
        process = True
        frame = vs.read() # read the most recent frame
        if np.array_equal(frame,display) == True: #Checks if this is a unique frame
            Duplicate = True
        else:
            display=frame #set the new frame to display so it can check if the next is new

            low=np.array([50,180,125])
            high=np.array([70,255,255])
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #Change image to HSV
            mask = cv2.inRange(hsv, low, high) #Apply Mask to image so only targets are white all else is black
            ct = None
            
            
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # Find the contours of the mask
            if len(cnts)!=0:  #only runs the following if you see something
                zzzzzz = 4
               

                too_small = []
                ct = 0
                for cts in cnts:
                    ### Find boundries and draw rectangle on image
                    
                    boxd,rect = contour(cts)#### Creates box form contours

                    heightList = list(rect)
                    height = heightList[0][1] + (heightList[1][1]/2)
                    
                    coordList.append(height)
                    boxList.append(boxd.astype(int))


                Max,idx = findMax(coordList)        
                cv2.drawContours(display,[boxList[idx]],0,(0,0,255),2) #Draws box on image these are the red boxes.  Its what you see
                
                        
            if Max != 0:
                screenText = 'Height=' + str(round(Max,1)) 
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

            
            #cv2.imshow("Mask", mask) ##look at mask image  ############ COMMENT OUT WHEN ON ROBOT !!!!!!!!!!!!!!!!!! Huge speed penalty
            cv2.imshow("Frame",display) ## look at what it sees ############ COMMENT OUT WHEN ON ROBOT !!!!!!!!!!!!!!!!!!

            
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

