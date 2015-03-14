#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

pin = 11 # GPIO pin used for footpedal

GPIO.setmode(GPIO.BOARD) 	# set mode to board numbering- this is compatible across different RPi versions
GPIO.setup(pin, GPIO.IN)		# set pin 3 as output, this is used for sensing the state of the footpedal

while True:
    print GPIO.input(pin)
    sleep(1)

