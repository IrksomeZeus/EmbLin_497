#!/usr/bin/env python
# Simple Etch-a-Sketch Program
# ECE497 Embedded 32bit Linux @ Rose-Hulman Institute of Technology
# Austin Yates  Sept. 5, 2016

import curses
import Adafruit_BBIO.GPIO as GPIO

def cursor_home():
    # Moves the cursor to the home position in the game.
    # Does not refresh.
    global cur_x
    global cur_y
    myscreen.move(4,3)
    cur_y = 0
    cur_x = 0

def move_cursor(dy, dx):
    # Moves the cursor as directed and writes an X at the new location
    global cur_x
    global cur_y
    global cleared
    global reset
    cleared = 0
    reset = 0
    dx = 2 * dx
    if (cur_y + dy >= y_grid) or (cur_y + dy < 0):
        return
    if (cur_x + dx >= (x_grid*2)) or (cur_x + dx < 0):
        return
    myscreen.move(cur_y + dy + 4, cur_x + dx + 3)
    cur_x = cur_x + dx
    cur_y = cur_y + dy
    myscreen.addstr('X')
    myscreen.refresh()

def size_prompt():
    # Prompts user for game board size.
    global y_grid
    global x_grid

    curses.echo()
    curses.nocbreak()

    myscreen.clear()
    myscreen.border(0)
    myscreen.addstr(0, 0, "Etch-a-Sketch v0.2")
    myscreen.addstr(4, 1, "Please enter the Y grid size: ")
    myscreen.refresh()
    y_grid = int(myscreen.getstr())
    myscreen.addstr(5, 1, "Please enter the X grid size: ")
    myscreen.refresh()
    x_grid = int(myscreen.getstr())

    curses.cbreak()
    curses.noecho()

def reset_board():
    # Resets board to the initial start conditions.
    global reset
    reset = 1
    size_prompt()

    myscreen.clear()
    myscreen.border(0)
    myscreen.addstr(0, 0, "Etch-a-Sketch v1.0")
    myscreen.addstr(1, 0, "Use w, a, s, and d to move the cursor. c to clear, r to reset, q to quit")
    for i in range(0, x_grid):
        myscreen.addstr(3, (i*2) + 3, str(i))
    for j in range(0, y_grid):
        myscreen.addstr(j + 4, 1, str(j))
    cursor_home()
    myscreen.addstr('X')
    myscreen.refresh()

def clear_board():
    # clears the board while keeping the cursor in the same place
    global cleared
    cleared = 1
    for k in range(0, y_grid):
        myscreen.move(k+4, 3)
        myscreen.clrtoeol()
    myscreen.move(cur_y + 4, cur_x + 3)
    myscreen.addstr('X')
    myscreen.refresh()

def clearHandler(channel):
    clear_board()

def moveLeft(channel):
    move_cursor(0, -1)

def moveRight(channel):
    move_cursor(0, 1)

def moveUp(channel):
    move_cursor(-1, 0)

def moveDown(channel):
    move_cursor(1, 0)


myscreen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)

x_grid = 8
y_grid = 8

cur_x = 0
cur_y = 0

cleared = 0

#setting descriptive names to pins being used
LEFT_BTN = "P9_11"
UP_BTN = "P9_13"
RIGHT_BTN = "P9_15"
DOWN_BTN = "P9_17"
CLEAR_BTN = "P9_18"

#setting up inputs
GPIO.setup(LEFT_BTN, GPIO.IN)
GPIO.setup(RIGHT_BTN, GPIO.IN)
GPIO.setup(UP_BTN, GPIO.IN)
GPIO.setup(DOWN_BTN, GPIO.IN)
GPIO.setup(CLEAR_BTN, GPIO.IN)

#setting up event detection
GPIO.add_event_detect(LEFT_BTN, GPIO.FALLING, callback=moveLeft, bouncetime=200)
GPIO.add_event_detect(RIGHT_BTN, GPIO.FALLING, callback=moveRight, bouncetime=200)
GPIO.add_event_detect(UP_BTN, GPIO.FALLING, callback=moveUp, bouncetime=200)
GPIO.add_event_detect(DOWN_BTN, GPIO.FALLING, callback=moveDown, bouncetime=200)
GPIO.add_event_detect(CLEAR_BTN, GPIO.FALLING, callback=clearHandler, bouncetime=200)

reset_board()

x = 0
keep_going = 1

while keep_going:
    x = myscreen.getch()

    if x == ord('w'):
        move_cursor(-1, 0)
    if x == ord('a'):
        move_cursor(0, -1)
    if x == ord('s'):
        move_cursor(1, 0)
    if x == ord('d'):
        move_cursor(0, 1)
    if x == ord('c'):
        clearHandler(None)
    if x == ord('r'):
        reset_board()
    if x == ord('q'):
        keep_going = 0

# Normal Exit

curses.echo()
curses.nocbreak()
curses.endwin()
# cleanup GPIO
GPIO.cleanup()
