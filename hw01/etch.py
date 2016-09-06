#!/usr/bin/env python
# Simple Etch-a-Sketch Program
# ECE497 Embedded 32bit Linux @ Rose-Hulman Institute of Technology
# Austin Yates  Sept. 5, 2016

import curses

myscreen = curses.initscr()

myscreen.border(0)
myscreen.addstr(12, 25, "Test String")
myscreen.refresh()
myscreen.getch()

curses.endwin()
