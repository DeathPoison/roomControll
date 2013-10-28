#!/usr/bin/env python
# -*- coding: utf-8 -*-  

HOST = "localhost"
PORT = 4223
UID = "eRN" # Change to your UID

import time

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_industrial_quad_relay import IndustrialQuadRelay

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    iqr = IndustrialQuadRelay(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Turn relays alternating on/off for 10 times with 100ms delay
    for i in range(1):
        iqr.set_value(0b0000000000001001) # turn on relay 0
        time.sleep(1)
        iqr.set_value(0b0000000000001010) # turn on relay 1
        time.sleep(1)
        
        iqr.set_value(0b0000000000000101) # turn off relay 0
        time.sleep(1)
        iqr.set_value(0b0000000000000110) # turn off relay 1
        time.sleep(1)
        iqr.set_value(0b0000000000000000) # turn off remote
        time.sleep(1)


    raw_input('Press key to exit\n') # Use input() in Python 3
    ipcon.disconnect()
