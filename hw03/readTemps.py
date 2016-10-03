#!/usr/bin/env python
# Simple Program to Read from the I2C temp sensors
# ECE497 Embedded 32bit Linux @ Rose-Hulman Institute of Technology
# Austin Yates  Oct. 3, 2016

from Adafruit_I2C import Adafruit_I2C

TEMP_REG = 0

temp101_0 = Adafruit_I2C(0x48, 2)
temp101_1 = Adafruit_I2C(0x49)
temp006_0 = Adafruit_I2C(0x40)

def toFahrenheit(celsius):
    f_temp = celsius * 1.8 + 32
    return f_temp

temp_0 = temp101_0.readS16(TEMP_REG)
print 'Raw value read: {}'.format(temp_0)

temp_0 = toFahrenheit(temp_0)
print 'Temp in F: {}'.format(temp_0)
