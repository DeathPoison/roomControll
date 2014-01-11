#!/usr/bin/env python
# -*- coding: utf-8 -*-

PORT   = 4223

from time      import strftime # use for clock simulation - shows time!
from time      import sleep    # use for delay in loops - wait for n sec.!
from threading import Thread   # use to create a single threat for time

import sys   # for unicode_to_kos0006u
import types # for unicode_to_kos0006u

from tinkerforge.ip_connection        import IPConnection
from tinkerforge.brick_master         import Master
from tinkerforge.bricklet_io16        import IO16
from tinkerforge.bricklet_rotary_poti import RotaryPoti
from tinkerforge.bricklet_lcd_20x4    import LCD20x4
from tinkerforge.bricklet_joystick    import Joystick
from tinkerforge.bricklet_industrial_quad_relay import IndustrialQuadRelay

try:
    from Board import Board as B
    from Menu import Menu as M
except ImportError as err:
    print err



if __name__ == "__main__":
    try:
        ### Connection for Menu
        MENU_HOST = "192.168.0.150" # Manually Set IP of Controller Board
        MENU_lcdUID = "gFt" # LCD Screen
        MENU_jskUID = "hAP" # Joystick
        ### END MENU CONNECTION

        # Connect to WLAN Controller
        MENU_ipcon = IPConnection() # Create IP connection

        lcd = LCD20x4(MENU_lcdUID, MENU_ipcon) # Create device object LCD
        jsk = Joystick(MENU_jskUID, MENU_ipcon) # Create device object JOYSTICK
        
        # Don't use device before ipcon is connected
        MENU_ipcon.connect(MENU_HOST, PORT) # Connect to brickd
        
        ### Connection for Board
        BOARD_HOST   = "192.168.0.111"
        BOARD_mstUID = "62eUEf" # master brick
        BOARD_io1UID = "ghh"    # io16
        BOARD_lcdUID = "9ew"    # lcd screen 20x4
        BOARD_iqrUID = "eRN"    # industrial quad relay
        #### END BOARD CONNECTION

        BOARD_ipcon = IPConnection() # Create IP connection

        mst = Master(BOARD_mstUID, BOARD_ipcon)   # Master Brick
        io1 = IO16(BOARD_io1UID, BOARD_ipcon)       # io16
        lcd1 = LCD20x4(BOARD_lcdUID, BOARD_ipcon)  # lcd20x4
        iqr = IndustrialQuadRelay(BOARD_iqrUID, BOARD_ipcon) # Create device object

        BOARD_ipcon.connect(BOARD_HOST, PORT) # Connect to brickd

        # create Menu instance with the nessesary Hardware # IPCON to close Tinker Connection
        M = M(jsk,lcd, MENU_ipcon) 

        # create Board instance 
        B = B(mst, io1, lcd1, iqr, BOARD_ipcon)        

        # On Press close Application
        raw_input('Press key to exit\n') # Use input() in Python 3
        M.quit()    # Stop Menu
        B.quit()    # Stop Board
        quit()

    except Exception as errtxt:
        print errtxt
