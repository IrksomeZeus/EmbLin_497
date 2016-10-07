#!/usr/bin/env python
# Simple Program to test LED Dot Matrix
# ECE497 Embedded 32bit Linux @ Rose-Hulman Institute of Technology
# Austin Yates  Oct. 5, 2016

import smbus
from time import sleep

# writes a block of data to the led matrix
def write_block(add, cmd, data):
    values = []
    for val in data:
        if val > 0xff:
            values.append(val & 0x00ff)
            values.append(val >> 8)
        else:
            values.append(val)
            values.append(0x00)
    bus.write_i2c_block_data(add, cmd, values)

DEVICE_ADDRESS = 0x70
DEVICE_DISP_RAM = 0x00
GREEN = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
ORANGE = [0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff]
RED = [0xff00, 0xff00, 0xff00, 0xff00, 0xff00, 0xff00, 0xff00, 0xff00]
OFF = [0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000]
SMILE_BMP=[0x3c, 0x42, 0x2889, 0x0485, 0x0485, 0x2889, 0x42, 0x3c]
FROWN_BMP=[0x3c00, 0x4200, 0x8520, 0x8900, 0x8900, 0x8520, 0x4200, 0x3c00]
NEUTRAL_BMP=[0x3c3c, 0x4242, 0xa9a9, 0x8989, 0x8989, 0xa9a9, 0x4242, 0x3c3c]

# Sets up display
bus = smbus.SMBus(2)

bus.write_byte(DEVICE_ADDRESS, 0x21) # turns on system oscillator
bus.write_byte(DEVICE_ADDRESS, 0xef) # full brightness
bus.write_byte(DEVICE_ADDRESS, 0x81) # display on, blink off

sleep(0.1)

# Writes a series of pictures to the matrix
write_block(DEVICE_ADDRESS, DEVICE_DISP_RAM, GREEN)
sleep(1)
write_block(DEVICE_ADDRESS, DEVICE_DISP_RAM, ORANGE)
sleep(1)
write_block(DEVICE_ADDRESS, DEVICE_DISP_RAM, RED)
sleep(1)
write_block(DEVICE_ADDRESS, DEVICE_DISP_RAM, FROWN_BMP)
sleep(1)
write_block(DEVICE_ADDRESS, DEVICE_DISP_RAM, NEUTRAL_BMP)
sleep(1)
write_block(DEVICE_ADDRESS, DEVICE_DISP_RAM, SMILE_BMP)

# Tests brightness control. Goes from full bright to min bright and back to full
for dimCmd in xrange(0xef, 0xdf, -1):
    bus.write_byte(DEVICE_ADDRESS, dimCmd)
    sleep(0.1)

for dimCmd in xrange(0xe1, 0xff):
    bus.write_byte(DEVICE_ADDRESS, dimCmd)
    sleep(0.1)
