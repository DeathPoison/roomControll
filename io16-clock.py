#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "aFh" # Change to your UID

from time import strftime # use for clock simulation - shows time!
from time import sleep # use for delay in loops - wait for n sec.!
from threading import Thread # use to create a single threat for time

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_io16 import IO16

class Clock():
    '''
       This class handles the 13Pin Clock Display

       example use to show 1337 on Display:

           c.Clock()
           c.show(1,3,3,7)

        @author LimeBlack as David Crimi

    '''
    def __init__(self):
  	    self.n = 80 # 80 loop ca. one second cause of sleep by 0.0125
  	    self.m = 160 # 80 loop ca. one second cause of sleep by 0.0125
  	    self.time = strftime('%H%M')
  	    self.t0 = self.time[0]
  	    self.t1 = self.time[1]
  	    self.t2 = self.time[2]
  	    self.t3 = self.time[3]

    def clearNum(self): # Clear all display
        io.set_port_configuration('a', (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7), 'o', False)
        io.set_port_configuration('b', (1 << 0) | (1 << 1), 'o', False)

    def port(self, port): # switch port - Displaygroup - Whitch of 4 Digits you wanna change?

        if port == 0: # set displayport (0) to pin port(4)
            port = 4
        if port == 1:
            port = 5
        if port == 2:
        	port = 6
        if port == 3:
        	port = 7

        self.ports = [] # list of all available ports
        self.ports.append(4)
        self.ports.append(5)
        self.ports.append(6)
        self.ports.append(7)

        self.ports.remove(port) # remove wanted port from death list

        for x in self.ports: # disable all unwanted ports!
            io.set_port_configuration('b', (1 << x) , 'o', True)
        io.set_port_configuration('b', (1 << port), 'o', False) # enable wanted port (displaygroup)

    def double(self): # show double points - enable port first!
        io.set_port_configuration('b', (1 << 1), 'o', True)
        io.set_port_configuration('a', (1 << 5), 'o', True)

    def zero(self): # show zero - enable port first!
        io.set_port_configuration('a', (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 6) | (1 << 7), 'o', True)

    def one(self): # show one - enable port first!
        io.set_port_configuration('a', (1 << 0) | (1 << 1), 'o', True)

    def two(self): # show two - enable port first!
        io.set_port_configuration('a', (1 << 0) | (1 << 2) | (1 << 3) | (1 << 6), 'o', True)
        io.set_port_configuration('b', (1 << 0), 'o', True)

    def three(self): # show three - enable port first!
        io.set_port_configuration('a', (1 << 0) | (1 << 2) | (1 << 3) | (1 << 1), 'o', True)
        io.set_port_configuration('b', (1 << 0), 'o', True)

    def four(self): # show four - enable port first!
        io.set_port_configuration('a', (1 << 0) | (1 << 1) | (1 << 7), 'o', True)
        io.set_port_configuration('b', (1 << 0), 'o', True)

    def five(self): # show five - enable port first!
        io.set_port_configuration('a', (1 << 1) | (1 << 2) | (1 << 3) | (1 << 7), 'o', True)
        io.set_port_configuration('b', (1 << 0), 'o', True)

    def six(self): # show six - enable port first!
        io.set_port_configuration('a', (1 << 1) | (1 << 2) | (1 << 3) | (1 << 6) | (1 << 7), 'o', True)
        io.set_port_configuration('b', (1 << 0), 'o', True)

    def seven(self): # show seven - enable port first!
        io.set_port_configuration('a', (1 << 0) | (1 << 1) | (1 << 2), 'o', True)

    def eight(self): # show eight - enable port first!
        io.set_port_configuration('a', (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 6) | (1 << 7), 'o', True)
        io.set_port_configuration('b', (1 << 0), 'o', True)

    def nine(self): # show nine - enable port first!
        io.set_port_configuration('a', (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 7), 'o', True)
        io.set_port_configuration('b', (1 << 0), 'o', True)

    def showDig(self, dig): # convert int in function for showing digit
        if dig == 0:
            self.zero()
        if dig == 1:
            self.one()
        if dig == 2:
            self.two()
        if dig == 3:
            self.three()
        if dig == 4:
            self.four()
        if dig == 5:
            self.five()
        if dig == 6:
            self.six()
        if dig == 7:
            self.seven()
        if dig == 8:
            self.eight()
        if dig == 9:
            self.nine()

    def show(self, p0, p1, p2, p3): # shows 4 digits on screen
        self.n = 80
        self.clearNum()

        while self.n >= 1:
            sleep(0.0125)

            self.port(0)
            self.showDig(p0)
            self.clearNum()

            self.port(1)
            self.showDig(p1)
            self.clearNum()

            self.port(2)
            self.showDig(p2)
            self.clearNum()

            #self.port(1)
            #self.double()
            #self.clearNum()

            self.port(3)
            self.showDig(p3)
            self.clearNum()

            self.n = self.n - 1
        return self

    def showTime(self): # display time without : on screen
        while self.m >= 1:
            sleep(0.0125)
            self.time = strftime('%H%M')
            self.t0 = self.time[0]
            self.t1 = self.time[1]
            self.t2 = self.time[2]
            self.t3 = self.time[3]
            #print self.t0
            self.show(int(self.t0), int(self.t1), int(self.t2), int(self.t3))
            #self.port(1) # have to add to show function cause this loop runs only 1 time in a sec
            #self.double()
            self.m = self.m -1
        return self

    def showsTime(self): # display time without : on screen
        self.time = strftime('%H%M')

        self.t0 = self.time[0]
        self.t1 = self.time[1]
        self.t2 = self.time[2]
        self.t3 = self.time[3]

        print self.time

        self.show(int(self.t0), int(self.t1), int(self.t2), int(self.t3))

        return self

#### STOP CLOCK CLASS #####

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    io = IO16(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Set pin 0 on port a to output low
    #io.set_port_configuration('b', 1 << 4, 'o', False)

# time examples
    #nine()
    #sleep(2)
    #c.double()
    #c.show(1,3,3,7)
    #c.port(1)
    #print strftime('%H%M')
   ##

    c = Clock()
    c.clearNum()
    c.showTime()

    raw_input('Press key to exit\n') # Use input() in Python 3
    #t.terminate() need to find a way stopping thread
    ipcon.disconnect()
    quit()