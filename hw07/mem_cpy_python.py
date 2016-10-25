#!/usr/bin/env python
# Program to test mem speed
# ECE497 Embedded 32bit Linux @ Rose-Hulman Institute of Technology
# Austin Yates  Oct 25, 2016


import Adafruit_BBIO.GPIO as GPIO

GPIO.setup('P9_28', GPIO.IN)
GPIO.setup('P9_27', GPIO.OUT)

def updateOutput(channel):
    GPIO.output('P9_27', GPIO.input('P9_28'))

GPIO.add_event_detect('P9_28', GPIO.BOTH, callback=updateOutput)

running = True
user_in = ''

while running:
    user_in = input("Input something to stop the program...")
    if user_in != '':
        running = False
