#!/usr/bin/env python
# Simple Etch-a-Sketch Program
# ECE497 Embedded 32bit Linux @ Rose-Hulman Institute of Technology
# Austin Yates  Sept. 5, 2016

import curses

myscreen = curses.initscr()
curses.noecho()
curses.cbreak()

x_grid = 8
y_grid = 8

cur_x = 0
cur_y = 0

def cursor_home():
    # Moves the cursor to the home position in the game.
    # Does not refresh.
    global cur_x
    global cur_y
    myscreen.move(4,2)
    cur_y = 0
    cur_x = 0

def move_cursor(dy, dx):
    # Moves the cursor as directed and writes an X at the new location
    global cur_x
    global cur_y
    dx = 2 * dx
    if (cur_y + dy >= y_grid) or (cur_y + dy < 0):
        return
    if (cur_x + dx >= (x_grid*2)) or (cur_x + dx < 0):
        return
    myscreen.move(cur_y + dy + 4, cur_x + dx + 2)
    cur_x = cur_x + dx
    cur_y = cur_y + dy
    myscreen.addstr('X')
    myscreen.refresh()

def reset_board():
    # Resets board to the initial start conditions.
    myscreen.clear()

    myscreen.border(0)
    myscreen.addstr(0, 0, "Etch-a-Sketch v0.1")
    myscreen.addstr(1, 0, "Use w, a, s, and d to move the cursor. c clears the board")
    for i in range(0, x_grid):
        myscreen.addstr(3, (i*2) + 2, str(i))
    for j in range(0, y_grid):
        myscreen.addstr(j + 4, 1, str(j))
    cursor_home()
    myscreen.addstr('X')
    myscreen.refresh()

reset_board()

x = 0
while x != ord('c'):
    x = myscreen.getch()

    if x == ord('w'):
        move_cursor(-1, 0)
    if x == ord('a'):
        move_cursor(0, -1)
    if x == ord('s'):
        move_cursor(1, 0)
    if x == ord('d'):
        move_cursor(0, 1)

curses.nocbreak()
curses.echo()
curses.endwin()
