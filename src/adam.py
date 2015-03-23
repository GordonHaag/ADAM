#!/usr/bin/env python

'''
todo: 
 - Right now, you have to Ctrl-c to kill it, that should change
 - 
'''
import RPi.GPIO as GPIO # used to communicate with footpedal
from time import sleep # used for debouncing of footpedal
import picamera # used to control camera
import os # used for filesystem manipulation
from sys import exit # used to exit
import subprocess # used to control external display process
# depends on imagemagick's display command


l = [d for d in os.listdir('/media') if d!='SETTINGS'] # get a list of mounted devices

if len(l) == 1: # One USB stick is mounted, continue
    d = '/media/'+l[0] 
    os.chdir(d) # change directory to USB stick
    print "Photos will be written to USB device at " + os.getcwd()

elif len(l) > 1: # More than one USB stick is mounted, exit with error
    sys.exit("Only one USB device can be inserted, I see "+ str(l))

elif len(l) < 1: # No USB stick is mounted, exit with error
    sys.exit("Please insert a USB device")


l = [int((p[:-4])) for p in os.listdir(d) if p[-4:] == '.jpg' and str(int(p[:-4])) == p[:-4]] # get a list of files that match our patter of N.jpg, where N is an integer

if l: # if we have already written files to this USB drive,
    n = max(l)+1 # we don't want to overwrite them
    print "Starting at " + str(n)
else: # otherwise 
    n=0 # start at zero




# GPIO setup
pedal = 11 # GPIO pin used for footpedal
GPIO.setmode(GPIO.BOARD) 	# set mode to board numbering- this is compatible across different RPi versions
GPIO.setup(pedal, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set pin 3 as output, this is used for sensing the state of the footpedal


def take_a_pic(n): # function to take a picture, write it to disk, display it, and wait for user to kill display
    with picamera.PiCamera() as camera:
        camera.resolution = (2592, 1944) # largest resolution available, 4x3 ratio
        camera.capture(str(n)+".jpg") # actually take the picture
        dis = subprocess.Popen(['display',str(n)+".jpg"]) # Show the picture
        GPIO.wait_for_edge(pedal, GPIO.RISING) # Wait for the user to press the pedal
        dis.kill() # get rid of the display


oldstate = GPIO.input(pedal)
preview = 5
while True:
    with picamera.PiCamera() as camera:
        camera.resolution = (640*2, 480*2) # smaller resolution for preview, it has to fit on screen
        camera.start_preview()
        GPIO.wait_for_edge(pedal, GPIO.RISING) # this event triggers a picture to be taken.
        camera.stop_preview()

    take_a_pic(n) # take the picture
    print n
    n +=1 # increment n, which is the file name
    '''        else:
                assert 1==0, "This is unreachable, GPIO error"
        sleep(0.05) # delay for debouncing
    '''

















