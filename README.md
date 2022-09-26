# Robotics2022


Main file: findMaxVision.py
Analyzes image frame utilizing the threaded PiVideoStream utility class which establishes image settings and lays the groundwork for the conversion of BGR to HSV color schemes.

PiVideoStream is threaded in an effort to utilize all 4 cores of the raspberry pi's processor, this is less necessary on the superior Pi 4's hardware but still is useful for centralizing settings and maximizing speeds.
This program will run at the maximum framerate the PiCamera can handle even on a Pi 3 (30 FPS @ 640x480, default camera mode) 

findMaxVision.py connects to FRC (First Robotics Competition) Roborio router to transmit data collected to robot for application.

Using HSV color scheme program seeks out bright green contours that will be reflected by reflective tape whena bright green neopixel camera is shined on it.
Neopixel is controlled by arduino nano or any adafruit device and can be controlled via a circuitpython script or the prepared arduino file within this repository.

alphabotWithi2cForBrightness.py was adapted to regulate the brightness of the neopixel should the HSV values exceed or fall below certain thresholds however this was deemed unnecessary and serial communication would be more effective than writing bytes through i2c.

From here the program uses the findMax(coords) function to take a list of y center points of each labeled contour (used boxes) with a set mimimum and maximum area to find the box on the top of the screen (minimum y) because that's the contour our robot is looking for.

After this calcproperties(x) are applied to use the center y coordinate of the box to approximate the distance in feet our robot is away.
This power function was derived by mapping center points to actual measured distances from a range of 0-40 feet in order to approximate distances.
Note a prior method used to find angle away from target was to use this distance with a pixel to inches conversion factor times the x distance the center of the target was from the center of the screen.
A conversion factor could be derived because the length of the target and it's distance above the ground were given values so they could be converted from pixels to inches.
From here a triangle was constructed and the opposite and adjecent sides are solved enabling the ability to derive an angle.
This however was still an approximation because the opposite side was an approximated distance value so it was determined to be better to physically measure the amount of degrees that go by per each x pixel (0.09375 degrees in a 640 px width frame) and use this to better approximate the angle away from the target by comparing the target's center point to the center of the screen.

Once relevant distance and angle data are found, depending on which side of the screen the object is (center x coordinate > (screenWidth/2)+5 = right, center x coordinate < (screenWidth/2)-5 = left, else is center) a negative or positive angle would be returned to the robot through a socket connection to the router as well as the distance and side of screen (right,left,or center)
