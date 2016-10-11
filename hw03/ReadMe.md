# Homework 3

## readTemps.py

Initially displays a readout from three temp sensors
  *TMP101 Sensors connected to I2C ports 0x48 and 0x49
  *TMP600 Sensor connected to port 0x4200

Then allows prompts the user to heat up or cool down the sensor with the address
0x48 in order to enable it's high and low temp alerts.

## led_etch.py

A version of the Etch-a-Sketch game that uses the LED matrix.

The game can be controlled using the buttons attached to the GPIO pins or the keyboard.
Clears can be done with the buttons, however, complete resets and quitting require the
keyboard.

| Pin | Direction |
|:---:|:---------:|
|P9_11|Left       |
|P9_13|Up         |
|P9_15|Right      |
|P9_17|Down       |
|P9_18|Clear      |

*Dimensions are now set to the LED matrix (8x8)*
