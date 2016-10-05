#!/usr/bin/env python
# Simple Program to Read from the I2C temp sensors
# ECE497 Embedded 32bit Linux @ Rose-Hulman Institute of Technology
# Austin Yates  Oct. 3, 2016

from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO
from time import sleep
from colorama import init, Fore, Style
import sys, getopt

init(autoreset=True) # initializes colorama for colored terminal text

TEMP_REG = 0
extraData = False
continuous = False
pollFreq = 5

temp101_0 = Adafruit_I2C(0x48, 2)
temp101_1 = Adafruit_I2C(0x49, 2)
temp006_0 = Adafruit_I2C(0x40, 2)
general = Adafruit_I2C(0x00, 2)

ALERT_0 = "P9_21"
GPIO.setup(ALERT_0, GPIO.IN)

# Parese command line arguements
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"vcf:",["verbose", "continuous", "pollFreq="])
except getopt.GetoptError:
    print 'readTemps.py -v verbose -c continuous -f <polling frequency in seconds>'
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-v", "--verbose"):
        extraData = True;
    elif opt in ("-c", "--continuous"):
        continuous = True;
    elif opt in ("-f", "--pollFreq"):
        pollFreq = int(arg)

def toFahrenheit(celsius):
    # Convert celsius temperature to fahrenheit
    f_temp = celsius * 1.8 + 32
    return f_temp

def toCelsius(fahrenheit):
    c_temp = (fahrenheit - 32) / 1.8
    return c_temp

# Read and display the temperature in degrees fahrenheit from the TMP101 sensor

def readSensor0(reg):
    if reg in {0, 2, 3}:
        data = temp101_0.readS16(reg)
        if data <= 0xff:
            data = data << 1
        else:
            data = temp101_0.reverseByteOrder(data)
            data = data >> 7
        data = data / 2
        return toFahrenheit(data)
    else:
        data = temp101_0.readU8(reg)
        return data

def readSensor1(reg):
    if reg in {0, 2, 3}:
        data = temp101_1.readS16(reg)
        if data <= 0xff:
            data = data << 1
        else:
            data = temp101_1.reverseByteOrder(data)
            data = data >> 7
        data = data / 2
        return toFahrenheit(data)
    else:
        data = temp101_1.readU8(reg)
        return data

def writeTemp_101(sensor, fahrenheit, reg):
    temp = int(round(toCelsius(fahrenheit)*2, 0))
    temp = temp << 7
    temp = sensor.reverseByteOrder(temp)
    sensor.write16(reg, temp)

print 'Sensor 0: {}F'.format(readSensor0(TEMP_REG))
print 'Sensor 1: {}F'.format(readSensor1(TEMP_REG))

temp_2 = temp006_0.readS16(1)
temp_2 = temp006_0.reverseByteOrder(temp_2)
temp_2 = temp_2 >> 2
temp_2 = temp_2 / 32
temp_2 = toFahrenheit(temp_2)

print 'Sensor 2: {}F'.format(temp_2)
print ""

# set config to interrupt mode with inverted alert
# Config Bits
#       D7      D6      D5      D4      D3      D2      D1      D0
#   OS/Alert    R1      R0      F1      F0      POL     TM      SD

# Set alerts
hiAlert = 82
loAlert = 76

writeTemp_101(temp101_0, loAlert, 2)
writeTemp_101(temp101_0, hiAlert, 3)

config = 0x06
temp101_0.write8(1, config)

a = readSensor0(TEMP_REG)
b = readSensor0(2)
c = readSensor0(3)
d = readSensor0(1)

print "Sensor 0"
print "Current temp: {}".format(a);
print "Low alert: {}".format(b);
print "High alert: {}".format(c);
print "Config Reg: {:08b}".format(d);
print ""

# Calibrate alerts based on current device state
alertBit = d >> 7
if alertBit:
    print "Config alert by lowering temperature below {}F...".format(b)
else:
    print "Config alert by raising temperature above {}F...".format(c)
while GPIO.input(ALERT_0) == 0:
    a = readSensor0(TEMP_REG)
    print 'Current Temp: {}F'.format(a)
    sleep(0.5)
print "\nDevice configured. Current temp bounds are {}F < T < {}F\nCurrent temp is {}F\n".format(b, c, a)

reported = 0
count = 0
while(True):
    if extraData:
        a = readSensor0(TEMP_REG)
        b = readSensor0(2)
        c = readSensor0(3)
        d = readSensor0(1)

        print "Current temp: {}".format(a);
        print "Low alert: {}".format(b);
        print "High alert: {}".format(c);
        print "Config Reg: {:08b}".format(d);
        print ""

    if GPIO.input(ALERT_0):
        if not reported:
            print Fore.RED + Style.BRIGHT + 'Temp out of normal bounds ({}<T<{}): {}F'.format(b, c, readSensor0(TEMP_REG))
        reported = 1;
    else:
        if reported or (not reported and count > 50 and continuous):
            a = readSensor0(TEMP_REG)
            if a >= hiAlert:
                print Fore.RED + 'Temp High: {}F'.format(a)
            elif a <= loAlert:
                print Fore.BLUE + 'Temp Low: {}F'.format(a)
            else:
                print 'Temp Normal: {}F'.format(b)
            count = 0
        count += 1
        reported = 0;

    sleep(0.1)
