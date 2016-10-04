#!/usr/bin/env python
# Simple Program to Read from the I2C temp sensors
# ECE497 Embedded 32bit Linux @ Rose-Hulman Institute of Technology
# Austin Yates  Oct. 3, 2016

from Adafruit_I2C import Adafruit_I2C

TEMP_REG = 0

temp101_0 = Adafruit_I2C(0x48, 2)
temp101_1 = Adafruit_I2C(0x49, 2)
temp006_0 = Adafruit_I2C(0x40, 2)

def toFahrenheit(celsius):
    # Convert celsius temperature to fahrenheit
    f_temp = celsius * 1.8 + 32
    return f_temp

# Read and display the temperature in degrees fahrenheit from the TMP101 sensor

temp_0 = temp101_0.readS16(TEMP_REG)
temp_0 = temp_0 & 0x01ff
temp_0 = toFahrenheit(temp_0)

temp_1 = temp101_1.readS16(TEMP_REG)
temp_1 = temp_1 & 0x01ff
temp_1 = toFahrenheit(temp_1)

print 'Sensor 0: {}F'.format(temp_0)
print 'Sensor 1: {}F'.format(temp_1)

# Read and display the temperature in degrees fahrenheit from the TMP006 sensor

temp_2 = temp006_0.readS16(1)
temp_2 = temp006_0.reverseByteOrder(temp_2)
temp_2 = temp_2 >> 2
temp_2 = temp_2 / 32
temp_2 = toFahrenheit(temp_2)

print 'Sensor 2: {}F'.format(temp_2)
