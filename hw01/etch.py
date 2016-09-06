#!/usr/bin/env python
# Simple Etch-a-Sketch Program
# ECE497 Embedded 32bit Linux @ Rose-Hulman Institute of Technology
# Austin Yates  Sept. 5, 2016

import curses

myscreen = curses.initscr()

x_grid = 8
y_grid = 8

myscreen.border(0)
myscreen.addstr(0, 0, "Etch-a-Sketch v1.0")
myscreen.addstr(1, 0, "Use W, A, S, and D to move the cursor. The Spacebar clears the board.")
for i in range(0, x_grid):
    myscreen.addstr(3, (i*2) + 2, str(i))
for j in range(0, y_grid):
    myscreen.addstr(j + 4, 1, str(j))
myscreen.refresh()
myscreen.getch()

curses.endwin()
