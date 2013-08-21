#!/usr/bin/env python
# -*- coding: utf-8 -*-  

HOST = "localhost"
PORT = 4223
alUID = "8RG" # Change to your UID
iqrUID = "eRN" # Change to your UID

import time

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_industrial_quad_relay import IndustrialQuadRelay

# Callback for illuminance less than 10 Lux
def cb_reached(illuminance):
    print('We have ' + str(illuminance/10.0) + ' Lux.')
    print('Too less bright, close the curtains!')

# Callback for illuminance without threshold
def cb_illuminance(ilu):
    tmpIlu = ilu/10 
    tmpBar = "::-::"
    while tmpIlu >= 0:
        tmpBar = tmpBar + "-:"
        tmpIlu = tmpIlu - 20

    print tmpBar

#    if ilu/10 >= 750:
 #       print(':|:|:|:|:|:|:|:|:|:')
  #  elif ilu/10 >= 600:
   #     print(':::::::::::::::::::')
    #else:
     #   print(':-.-.-.-.-.-.-.-.-:')

    #print('Illuminance: ' + str(ilu/10) + ' Lux!')

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    al = AmbientLight(alUID, ipcon) # Create device object
    iqr = IndustrialQuadRelay(iqrUID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Get threshold callbacks with a debounce time of 10 seconds (10000ms)
    # al.set_debounce_period(100)
    al.set_illuminance_callback_period(10)

    # Register threshold reached callback to function cb_reached
    al.register_callback(al.CALLBACK_ILLUMINANCE_REACHED, cb_reached)
    al.register_callback(al.CALLBACK_ILLUMINANCE, cb_illuminance)

    # Configure threshold for "greater than 200 Lux" (unit is Lux/10)
    # al.set_illuminance_callback_threshold('<', 10*10, 0)
    
    # Turn relays alternating on/off for 10 times with 100ms delay
    #for i in range(10):
    #    time.sleep(0.1)
    #    iqr.set_value(1 << 0)
    #    time.sleep(0.1)
    #    iqr.set_value(1 << 1)
    #    time.sleep(0.1)
    #    iqr.set_value(1 << 2)
    #    time.sleep(0.1)
    #    iqr.set_value(1 << 3)


    raw_input('Press key to exit\n') # Use input() in Python 3
    ipcon.disconnect()
