#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

pin = 11 # GPIO pin used for footpedal

GPIO.setmode(GPIO.BOARD) 	# set mode to board numbering- this is compatible across different RPi versions
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set pin 3 as output, this is used for sensing the state of the footpedal

oldstate = GPIO.input(pin)
while True:
    state = GPIO.input(pin)
    if oldstate != state:
        print ["up", "down"][state] # 
        oldstate = state
    sleep(0.05) # delay for debouncing
