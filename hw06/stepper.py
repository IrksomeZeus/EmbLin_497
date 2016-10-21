#!/usr/bin/env python
# Simple Program to control a stepper motor
# ECE497 Embedded 32bit Linux @ Rose-Hulman Institute of Technology
# Austin Yates  Oct. 20, 2016

import Adafruit_BBIO.GPIO as GPIO
from time import sleep

startBtn = 'P9_18'
controller = ['P9_22', 'P9_24', 'P9_26', 'P9_28']

states = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]];
statesHiTorque = [[1,1,0,0], [0,1,1,0], [0,0,1,1], [1,0,0,1]];
statesHalfStep = [[1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0],
                  [0,0,1,0], [0,0,1,1], [0,0,0,1], [1,0,0,1]];

global currentState
global steps
global curDirection
delay = 0.01 # delay between rotate commands being sent; adjust for system
motorRevSteps = 32 # steps for internal motor in 4 step mode
outputRevSteps = motorRevSteps * 64 # steps per output shaft rotation
CW = 1
CCW = -1

def main():
    init()

    print "Push Start Button..."
    while GPIO.input(startBtn):
        pass
    print "Rotating.."
    rotateRevs()
    rotateRevs(CCW)
    print "Done."


def init():
    global currentState
    global steps
    global curDirection
    # Setup GPIO
    GPIO.setup(startBtn, GPIO.IN)
    for port in controller:
        GPIO.setup(port, GPIO.OUT)
    currentState = 0
    steps = 0
    curDirection = CW
    goToState(states[0])

def rotate(direction):
    global currentState
    global curDirection
    curDirection = direction
    currentState += direction
    if currentState >= len(states):
        currentState = 0
    elif currentState < 0:
        currentState = len(states) - 1
    goToState(states[currentState])

def goToState(state):
    global steps
    for i, port in enumerate(controller):
        GPIO.output(port, state[i])
    steps += curDirection

def rotateRevs(direction=CW, revs=1):
    end = steps + revs * outputRevSteps * direction
    while end != steps:
        rotate(direction)
        sleep(delay)


if __name__ == '__main__':
    try:
        main()
    finally:
        goToState([0,0,0,0])
        GPIO.cleanup()
