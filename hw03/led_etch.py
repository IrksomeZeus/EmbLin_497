#!/usr/bin/env python
# Etch-a-Sketch Game that uses the LED Matrix

import curses
import smbus
import Adafruit_BBIO.GPIO as GPIO
from time import sleep

LEFT_BTN = "P9_11"
UP_BTN = "P9_13"
RIGHT_BTN = "P9_15"
DOWN_BTN = "P9_17"
CLEAR_BTN = "P9_18"

DEVICE_ADDRESS = 0x70
RAM_ADDRESS = 0x00
ALL_OFF = [0x0001, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000] # Doesn't seem to work with the placeholder 1 as the first element for some reason

x_grid = 8
y_grid = 8
cur_x = 0
cur_y = 0

def main(stdscr):
    global screen
    global bus
    global matrix
    matrix = ALL_OFF[1:]
    screen = stdscr
    bus = init()
    resetBoard()

    x = 0
    while True:
        x = screen.getch()

        if x == ord('w'):
            moveCursor(-1, 0)
        if x == ord('a'):
            moveCursor(0, -1)
        if x == ord('s'):
            moveCursor(1, 0)
        if x == ord('d'):
            moveCursor(0, 1)
        if x == ord('c'):
            clearBoard()
        if x == ord('r'):
            resetBoard()
        if x == ord('q'):
            break

        GPIO.cleanup()

def init():

    GPIO.setup(LEFT_BTN, GPIO.IN)
    GPIO.setup(RIGHT_BTN, GPIO.IN)
    GPIO.setup(UP_BTN, GPIO.IN)
    GPIO.setup(DOWN_BTN, GPIO.IN)
    GPIO.setup(CLEAR_BTN, GPIO.IN)

    GPIO.add_event_detect(LEFT_BTN, GPIO.FALLING, callback=moveLeft, bouncetime=200)
    GPIO.add_event_detect(RIGHT_BTN, GPIO.FALLING, callback=moveRight, bouncetime=200)
    GPIO.add_event_detect(UP_BTN, GPIO.FALLING, callback=moveUp, bouncetime=200)
    GPIO.add_event_detect(DOWN_BTN, GPIO.FALLING, callback=moveDown, bouncetime=200)
    GPIO.add_event_detect(CLEAR_BTN, GPIO.FALLING, callback=clearHandler, bouncetime=200)

    bus = smbus.SMBus(2)

    bus.write_byte(DEVICE_ADDRESS, 0x21) # turns on system oscillator
    bus.write_byte(DEVICE_ADDRESS, 0xef) # full brightness
    bus.write_byte(DEVICE_ADDRESS, 0x81) # display on, blink off

    sleep(0.1)

    return bus

def moveLeft(channel):
    moveCursor(0, -1)

def moveRight(channel):
    moveCursor(0, 1)

def moveUp(channel):
    moveCursor(-1, 0)

def moveDown(channel):
    moveCursor(1, 0)

def clearHandler(channel):
    clearBoard()

def resetBoard():
    global matrix
    screen.clear()
    screen.border(0)
    screen.addstr(0, 0, "LED Etch-a-Sketch")
    screen.addstr(1, 0, "Use w, a, s, and d or the buttons to move the cursor.")
    screen.addstr(2, 0, "c to clear, r to reset, and q to quit")
    screen.addstr(3, 0, "The 5th button will clear the board or reset depending on board state.")

    for i in xrange(0, x_grid):
        screen.addstr(5, (i*2) + 3, str(i))
    for j in xrange(0, y_grid):
        screen.addstr(j + 6, 1, str(i))

    cursorHome(screen)

    screen.addstr('X')
    matrix = ALL_OFF[1:]
    writeMatrix()
    cursorAt(cur_x, cur_y, 'on')
    writeMatrix()
    screen.refresh()

def clearBoard():
    global cleared
    global matrix

    # clears curses screen
    for k in xrange(0, y_grid):
        screen.move(k+6, 3)
        screen.clrtoeol()

    # clears LED display
    matrix = []
    matrix = ALL_OFF[1:]
    writeMatrix()

    # restore cursor
    screen.move(cur_y + 6, cur_x + 3)
    screen.addstr('X')
    screen.refresh()
    cursorAt(cur_x, cur_y, 'on')

def moveCursor(dy, dx):
    # Moves the cursor on display and LED matrix
    global cur_x
    global cur_y

    dx = 2 * dx
    if (cur_y + dy >= y_grid) or (cur_y + dy < 0):
        return
    if (cur_x + dx >= (x_grid*2)) or (cur_x + dx < 0):
        return

    cursorAt(cur_x, cur_y, 'green')
    screen.move(cur_y + dy + 6, cur_x + dx + 3)
    cur_x = cur_x + dx
    cur_y = cur_y + dy
    screen.addstr('X')
    screen.refresh()
    cursorAt(cur_x, cur_y, 'on')


def cursorAt(x, y, color):
    global matrix
    bit = 1
    bit = bit << ((x/2))

    if color == 'red':
        matrix[y] = matrix[y] ^ (bit << 8)
    elif color == 'green':
        matrix[y] = matrix[y] ^ bit
    elif color == 'off':
        matrix[y] = 0x0000
    elif color == 'on':
        matrix[y] = matrix[y] | (bit << 8)
        matrix[y] = matrix[y] ^ bit
    writeMatrix()

def cursorHome(screen):
    # Moves the cursor to the home position in the game.
    # Does not refresh.
    global cur_x
    global cur_y
    screen.move(6,3)
    cur_y = 0
    cur_x = 0

def writeBlock(add, cmd, data):
    values = []
    for val in matrix:
        if val > 0xff:
            values.append(val & 0x00ff)
            values.append(val >> 8)
        else:
            values.append(val)
            values.append(0x00)
    bus.write_i2c_block_data(add, cmd, values)

def writeMatrix():
    writeBlock(DEVICE_ADDRESS, RAM_ADDRESS, matrix)


if __name__ == '__main__':
    curses.wrapper(main)
