#!/usr/bin/env python
# -*- coding: utf-8 -*-


from time      import strftime # use for clock simulation - shows time!
from time      import sleep    # use for delay in loops - wait for n sec.!
from threading import Thread   # use to create a single threat for time

import sys   # for unicode_to_kos0006u
import types # for unicode_to_kos0006u

import socket # check if tinker is available
from twisted.internet import reactor, protocol # for twisted connection!

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

def isOpen(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False

class master():
    """docstring for master"""
    def __init__(self):
        #super(master, self).__init__()
        print 'init...'
        self.PORT   = 4223
        self.MENU_running = False
        self.BOARD_running = False

        ### Connection for Menu
        self.MENU_HOST   = "192.168.0.150" # Manually Set IP of Controller Board
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

        #print self.start()
        return
        
    def start(self):
        if self.BOARD_running: print 'Board already running!'
        else: self.startBoard(); print 'Board Started!'

        if self.MENU_running: print 'Menu already running!'
        else: self.startMenu(); print 'Menu Started!'
        return 'Started!'

    def status(self):
        return 'Board: '+str(self.BOARD_running)+'\nMenu: '+str(self.MENU_running)
    
    def startBoard(self):
        if self.BOARD_running: return 'Board already running!'

        if isOpen(self.BOARD_HOST, self.PORT):
            
            self.BOARD_running = True

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
    
    def startMenu(self):
        if self.MENU_running: return 'Menu already running!'

        if isOpen(self.MENU_HOST, self.PORT):

            self.MENU_running = True

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

    def stop(self):
        print 'stopping devices...'
        if self.MENU_running: 
            self.MENU_running = False
            self.MM.quit()
        if self.BOARD_running:
            self.BOARD_running = False
            self.BB.quit()    # Stop Board
        #quit()
        return 'successfully stopped'        

class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""
    
    def dataReceived(self, data):
        print data
        if data in function_dict:
            print 'found command!'
            responseOFdata = function_dict[data]()
            print responseOFdata
            self.transport.write('[color=CCFF33]Command: '+data+'[/color]\n')
            self.transport.write('Response is: \n[color=00FFFF]')
            self.transport.write(responseOFdata+'[/color]\n')
        else:
            print 'dont know what to do with this post...'
            print "As soon as any data is received, write it back."
            self.transport.write('[color=CC3300]Not fount: '+data+'![/color]')

if __name__ == "__main__":
    try:


        masterInstance = master()
        print masterInstance.status()
        # On Press close Application

        function_dict = {
            'start':masterInstance.start, 
            'status':masterInstance.status, 
            'startMenu':masterInstance.startMenu, 
            'startBoard':masterInstance.startBoard,
            'stop':masterInstance.stop, 
        }

                        #if data in function_dict:#== 'status':
                        #    function_dict[data]()
                        #    print "process will staart!"
                            #print data
                            #connection.sendall(data)

        
        """This runs the protocol on port 8000"""
        factory = protocol.ServerFactory()
        factory.protocol = Echo
        reactor.listenTCP(8000,factory)
        reactor.run()

        #masterInstance.stop()
    except Exception as errtxt:
        print errtxt
