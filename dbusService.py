#!/usr/bin/env python
# -*- coding: utf-8 -*-
# myservice.py
# simple python-dbus service that exposes 1 method called hello()

import gtk    # Linux DBus Service
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

from time      import strftime # use for clock simulation - shows time!
from time      import sleep    # use for delay in loops - wait for n sec.!
from threading import Thread   # use to create a single threat for time

import sys   # for unicode_to_kos0006u
import types # for unicode_to_kos0006u

import socket # check if tinker is available

from tinkerforge.ip_connection        import IPConnection # Tinker bindings
from tinkerforge.brick_master         import Master
from tinkerforge.bricklet_io16        import IO16
from tinkerforge.bricklet_rotary_poti import RotaryPoti
from tinkerforge.bricklet_lcd_20x4    import LCD20x4
from tinkerforge.bricklet_joystick    import Joystick
from tinkerforge.bricklet_industrial_quad_relay import IndustrialQuadRelay

try: # import myown Board and Menu Library!
    from Board import Board as B
    from Menu import Menu as M
except ImportError as err:
    print err

def isOpen(ip,port): # check socket  # used to check if tinker is online
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False

class MyDBUSService(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName('org.limeblack.roomcontroll', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/org/limeblack/roomcontroll')
        try:
            print 'Start initalisation'
            
            self.BoardIsRunning = False
            self.MenuIsRunning  = False

            self.PORT   = 4223
            
            ### Connection for Menu
            self.MENU_HOST = "192.168.0.150" # Manually Set IP of Controller Board
            self.MENU_lcdUID = "gFt" # LCD Screen
            self.MENU_jskUID = "hAP" # Joystick
            ### END MENU CONNECTION

            
            ### Connection for Board
            self.BOARD_HOST   = "192.168.0.111"
            self.BOARD_mstUID = "62eUEf" # master brick
            self.BOARD_io1UID = "ghh"    # io16
            self.BOARD_lcdUID = "9ew"    # lcd screen 20x4
            self.BOARD_iqrUID = "eRN"    # industrial quad relay
            #### END BOARD CONNECTION

            
            if isOpen(self.BOARD_HOST, self.PORT):
                
                self.BoardIsRunning = True

                self.BOARD_ipcon = IPConnection() # Create IP connection

                self.mst = Master(self.BOARD_mstUID, self.BOARD_ipcon)   # Master Brick
                self.io1 = IO16(self.BOARD_io1UID, self.BOARD_ipcon)       # io16
                self.lcd1 = LCD20x4(self.BOARD_lcdUID, self.BOARD_ipcon)  # lcd20x4
                self.iqr = IndustrialQuadRelay(self.BOARD_iqrUID, self.BOARD_ipcon) # Create device object

                self.BOARD_ipcon.connect(self.BOARD_HOST, self.PORT) # Connect to brickd
                
                # create Board instance 
                self.BB = B(self.mst, self.io1, self.lcd1, self.iqr, self.BOARD_ipcon)        
            else:
                print 'board offline'
            

            if isOpen(self.MENU_HOST, self.PORT):

                self.MenuIsRunning = True

                # Connect to WLAN Controller
                self.MENU_ipcon = IPConnection() # Create IP connection

                self.lcd = LCD20x4(self.MENU_lcdUID, self.MENU_ipcon) # Create device object LCD
                self.jsk = Joystick(self.MENU_jskUID, self.MENU_ipcon) # Create device object JOYSTICK
                
                # Don't use device before ipcon is connected
                self.MENU_ipcon.connect(self.MENU_HOST, self.PORT) # Connect to brickd

                # create Menu instance with the nessesary Hardware # IPCON to close Tinker Connection
                self.MM = M(self.jsk, self.lcd, self.MENU_ipcon) 
            else:
                print 'menu is offline'                 

            print 'Initialisation ready!'

        except Exception as errtxt:
            print errtxt

    @dbus.service.method('org.limeblack.roomcontroll')
    def hello(self):
        return "Hello, World!"
    
    @dbus.service.method('org.limeblack.roomcontroll')
    def startBoard(self):
        if self.BoardIsRunning: return 'Board already running!'

        if isOpen(self.BOARD_HOST, self.PORT):
            
            self.BoardIsRunning = True

            self.BOARD_ipcon = IPConnection() # Create IP connection

            self.mst = Master(self.BOARD_mstUID, self.BOARD_ipcon)   # Master Brick
            self.io1 = IO16(self.BOARD_io1UID, self.BOARD_ipcon)       # io16
            self.lcd1 = LCD20x4(self.BOARD_lcdUID, self.BOARD_ipcon)  # lcd20x4
            self.iqr = IndustrialQuadRelay(self.BOARD_iqrUID, self.BOARD_ipcon) # Create device object

            self.BOARD_ipcon.connect(self.BOARD_HOST, self.PORT) # Connect to brickd
            
            # create Board instance 
            self.BB = B(self.mst, self.io1, self.lcd1, self.iqr, self.BOARD_ipcon)        
        else:
            return 'Board is offline'
        return "Hello, Board successfully started!"
    
    @dbus.service.method('org.limeblack.roomcontroll')
    def startMenu(self):
        if self.MenuIsRunning: return 'Menu already running!'

        if isOpen(self.MENU_HOST, self.PORT):

            self.MenuIsRunning = True

            # Connect to WLAN Controller
            self.MENU_ipcon = IPConnection() # Create IP connection

            self.lcd = LCD20x4(self.MENU_lcdUID, self.MENU_ipcon) # Create device object LCD
            self.jsk = Joystick(self.MENU_jskUID, self.MENU_ipcon) # Create device object JOYSTICK
            
            # Don't use device before ipcon is connected
            self.MENU_ipcon.connect(self.MENU_HOST, self.PORT) # Connect to brickd

            # create Menu instance with the nessesary Hardware # IPCON to close Tinker Connection
            self.MM = M(self.jsk, self.lcd, self.MENU_ipcon) 
        else:
            return 'Menu is offline'  

        return "Hello, Menu successfully started!"



    @dbus.service.method('org.limeblack.roomcontroll')
    def bye(self):
        if self.BoardIsRunning: 
            self.BoardIsRunning = False
            self.BB.quit()
        if self.MenuIsRunning:  
            self.MenuIsRunning = False
            self.MM.quit()

        return "Shutdown successfully!"

DBusGMainLoop(set_as_default=True)
myservice = MyDBUSService()
gtk.main()
