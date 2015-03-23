#!/usr/bin/env python

'''
todo: 
 - write in /ADAM directory on drive
 - 
'''
import RPi.GPIO as GPIO # used to communicate with footpedal
from time import sleep # used for debouncing of footpedal
import picamera # used to control camera
import os # used for filesystem manipulation
from sys import exit # used to exit
import subprocess


l = [d for d in os.listdir('/media') if d!='SETTINGS'] # get a list of mounted devices

if len(l) == 1: # One USB stick is mounted, continue
    d = '/media/'+l[0]
    os.chdir(d) # change directory to USB stick
    print "Photos will be written to USB device at " + os.getcwd()

elif len(l) > 1: # More than one USB stick is mounted, exit with error
    sys.exit("Only one USB device can be inserted, I see "+ str(l))

elif len(l) < 1: # No USB stick is mounted, exit with error
    sys.exit("Please insert a USB device")


l = [int((p[:-4])) for p in os.listdir(d) if p[-4:] == '.jpg' and str(int(p[:-4])) == p[:-4]]
print l
if l:
    n = max(l)+1
    print "Starting at " + str(n)
else:
    n=0




# GPIO setup
pedal = 11 # GPIO pin used for footpedal
GPIO.setmode(GPIO.BOARD) 	# set mode to board numbering- this is compatible across different RPi versions
GPIO.setup(pedal, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set pin 3 as output, this is used for sensing the state of the footpedal


def take_a_pic(n):
    with picamera.PiCamera() as camera:
        '''
                camera.resolution = (640*2, 480*2)
                camera.start_preview()
                sleep(preview)
                camera.stop_preview()
        '''
        camera.resolution = (2592, 1944)
        camera.capture(str(n)+".jpg")
        dis = subprocess.Popen(['display',str(n)+".jpg"]) # Show the most recent image
        GPIO.wait_for_edge(pedal, GPIO.RISING) # Wait for the user to press the pedal
        dis.kill() # get rid of the display


n = 0
oldstate = GPIO.input(pedal)
preview = 5
while True:
    '''
        state = GPIO.input(pedal)
        if oldstate != state:
            print ["up", "down"][state] # 
            oldstate = state
            if state == 0: # pedal is up
                pass
            elif state == 1: # pedal is down
    '''
    with picamera.PiCamera() as camera:
        camera.resolution = (640*2, 480*2)
        camera.start_preview()
        GPIO.wait_for_edge(pedal, GPIO.RISING)
        camera.stop_preview()

    take_a_pic(n)
    print n
    n +=1
    '''        else:
                assert 1==0, "This is unreachable, GPIO error"
        sleep(0.05) # delay for debouncing
    '''

















