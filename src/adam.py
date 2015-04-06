#!/usr/bin/env python

import RPi.GPIO as GPIO  # used to communicate with footpedal
from time import sleep  # used for debouncing of footpedal
import picamera  # used to control camera
import os  # used for filesystem manipulation
import sys  # used to exit
import subprocess  # used to control external display process
# depends on imagemagick's display command

# GPIO setup
pedal = 11  # GPIO pin used for footpedal
# set mode to board numbering- this is compatible across different RPi versions
GPIO.setmode(GPIO.BOARD)
# set pin 3 as output, this is used for sensing the state of the footpedal
GPIO.setup(pedal, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def take_a_pic(n):
    """Function to take a picture, write it to disk, display it, and wait for
user to kill display"""
    with picamera.PiCamera() as camera:
        camera.resolution = (2592, 1944)  # largest res available, 4x3 ratio
        camera.capture(str(n)+".jpg")  # actually take the picture
        dis = subprocess.Popen(['display', str(n)+".jpg"])  # Show the picture
        GPIO.wait_for_edge(pedal, GPIO.RISING)  # Wait for pedal press
        dis.kill()  # get rid of the display


def acknowledged_exit(message):
    """Function to make the user acknowledge an error before exiting"""
    print message
    print 'Press footpedal to exit...'
    GPIO.wait_for_edge(pedal, GPIO.RISING)
    sys.exit()

# get a list of mounted devices
l = [d for d in os.listdir('/media') if d != 'SETTINGS']

if len(l) == 1:  # One USB stick is mounted, continue
    d = '/media/'+l[0]
    os.chdir(d)  # change directory to USB stick
    print "Photos will be written to USB device at " + os.getcwd()

elif len(l) > 1:  # More than one USB stick is mounted, exit with error
    acknowledged_exit("Only one USB device can be inserted, I see " + str(l))

elif len(l) < 1:  # No USB stick is mounted, exit with error
    acknowledged_exit("Please insert a USB device")

# get a list of files that match our patter of N.jpg, where N is an integer
l = [int((p[:-4])) for p in os.listdir(d) if p[-4:] == '.jpg' and
     str(int(p[:-4])) == p[:-4]]

if l:  # if we have already written files to this USB drive,
    n = max(l)+1  # we don't want to overwrite them
    print "Starting at " + str(n)
else:  # otherwise
    n = 0  # start at zero


while True:
    with picamera.PiCamera() as camera:
        camera.resolution = (640*2, 480*2)  # smaller res, has to fit on screen
        camera.start_preview()
        GPIO.wait_for_edge(pedal, GPIO.RISING)  # this event triggers a picture
        camera.stop_preview()
    try:
        take_a_pic(n)  # take the picture
        print n
        n += 1  # increment n, which is the file name
    except IOError:
            acknowledged_exit("USB removed")

