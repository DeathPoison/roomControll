#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST   = "localhost"
PORT   = 4223
mstUID = "62eUEf" # master brick
ioUID  = "aFh" # io16
lcdUID = "9ew" # lcd screen 20x4
rpUID  = "8Cu" # rotary Poti

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

#### START CLOCK CLASS ####
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
        self.time = strftime('%H%M') # get time

        self.t0 = self.time[0] # each 
        self.t1 = self.time[1] # digit 
        self.t2 = self.time[2] # one 
        self.t3 = self.time[3] # number

        self.show(int(self.t0), int(self.t1), int(self.t2), int(self.t3)) # show time for one sec.
        return self

#### STOP CLOCK CLASS #####

#### START LCD20x4 KEY CALLBACK ######
def cb_pressed(i):
    #print "Pressed: " + str(i)
    if i == 0 :
        print "pressed button left"
    elif i == 1: 
        # Turn backlight on
        if lcd.is_backlight_on() == 1: 
            lcd.backlight_off()
        else:
            lcd.backlight_on()
    elif i == 2:
        c = Clock()
        c.clearNum()
        t = Thread(target=c.showTime) # can replace last none with ('MyArgument', 1)
        t.start()

def cb_released(i):
    #print "Released: " + str(i)
    if i == 0 :
        print "released button left"
    elif i == 1: 
        print "released middle button"
    #elif i == 2:
        #print "released button on right"

#### STOP LCD 20x4 KEY CALLBACK ######


###### Register Callback IO 16 Port B2 - Door ######
def cb_interrupt(port, interrupt_mask, value_mask):
    ## only debug
    #print "Port: " + port + " by InterMask: " + str(bin(interrupt_mask)) + " with Value: " + str(bin(value_mask))
    value = str(bin(value_mask))
    #print value[-3] # should be the door
    if value[-3] == "1":# and value[7] == "1":
        lcd.write_line(3, 0, "                    ") # 20x Blank to clear last line
        lcd.write_line(3, 0, unicode_to_ks0066u('Door: Open!'))
    elif value[-3] == "0":# and value[7] == "0":
        lcd.write_line(3, 0, "                    ") # 20x Blank to clear last line
        lcd.write_line(3, 0, unicode_to_ks0066u('Door: Closed... =)'))
###### STOP IO16 Callback ######



########### SYSTEM COMMANDS :P ##############


def timeout(i):
    print "sleeping 5 sec from thread %d" % i
    sleep(5)
    print "finished sleeping from thread %d" % i

def stopApp():
	raw_input('Press key to exit\n') # Use input() in Python 3
	#t.terminate() need to find a way stopping thread
	ipcon.disconnect()
	quit()

#### START UNICODE TO KOS0006U FOR LCD20x4 ######
# Maps a Python string to the LCD charset
def unicode_to_ks0066u(string):
    if sys.hexversion < 0x03000000:
        byte = lambda x: chr(x)
        ks0066u = ''

        if type(string) != types.UnicodeType:
            code_points = unicode(string, 'UTF-8')
        else:
            code_points = string
    else:
        byte = lambda x: bytes([x])
        ks0066u = bytes()
        code_points = string

    for code_point in code_points:
        code_point = ord(code_point)

        # ASCII subset from JIS X 0201
        if code_point >= 0x0020 and code_point <= 0x007e:
            # The LCD charset doesn't include '\' and '~', use similar characters instead
            mapping = {
                0x005c : byte(0xa4), # REVERSE SOLIDUS maps to IDEOGRAPHIC COMMA
                0x007e : byte(0x2d)  # TILDE maps to HYPHEN-MINUS
            }

            try:
                c = mapping[code_point]
            except KeyError:
                c = byte(code_point)
        # Katakana subset from JIS X 0201
        elif code_point >= 0xff61 and code_point <= 0xff9f:
            c = byte(code_point - 0xfec0)
        # Special characters
        else:
            mapping = {
                0x00a5 : byte(0x5c), # YEN SIGN
                0x2192 : byte(0x7e), # RIGHTWARDS ARROW
                0x2190 : byte(0x7f), # LEFTWARDS ARROW
                0x00b0 : byte(0xdf), # DEGREE SIGN maps to KATAKANA SEMI-VOICED SOUND MARK
                0x03b1 : byte(0xe0), # GREEK SMALL LETTER ALPHA
                0x00c4 : byte(0xe1), # LATIN CAPITAL LETTER A WITH DIAERESIS
                0x00e4 : byte(0xe1), # LATIN SMALL LETTER A WITH DIAERESIS
                0x00df : byte(0xe2), # LATIN SMALL LETTER SHARP S
                0x03b5 : byte(0xe3), # GREEK SMALL LETTER EPSILON
                0x00b5 : byte(0xe4), # MICRO SIGN
                0x03bc : byte(0xe4), # GREEK SMALL LETTER MU
                0x03c2 : byte(0xe5), # GREEK SMALL LETTER FINAL SIGMA
                0x03c1 : byte(0xe6), # GREEK SMALL LETTER RHO
                0x221a : byte(0xe8), # SQUARE ROOT
                0x00b9 : byte(0xe9), # SUPERSCRIPT ONE maps to SUPERSCRIPT (minus) ONE
                0x00a4 : byte(0xeb), # CURRENCY SIGN
                0x00a2 : byte(0xec), # CENT SIGN
                0x2c60 : byte(0xed), # LATIN CAPITAL LETTER L WITH DOUBLE BAR
                0x00f1 : byte(0xee), # LATIN SMALL LETTER N WITH TILDE
                0x00d6 : byte(0xef), # LATIN CAPITAL LETTER O WITH DIAERESIS
                0x00f6 : byte(0xef), # LATIN SMALL LETTER O WITH DIAERESIS
                0x03f4 : byte(0xf2), # GREEK CAPITAL THETA SYMBOL
                0x221e : byte(0xf3), # INFINITY
                0x03a9 : byte(0xf4), # GREEK CAPITAL LETTER OMEGA
                0x00dc : byte(0xf5), # LATIN CAPITAL LETTER U WITH DIAERESIS
                0x00fc : byte(0xf5), # LATIN SMALL LETTER U WITH DIAERESIS
                0x03a3 : byte(0xf6), # GREEK CAPITAL LETTER SIGMA
                0x03c0 : byte(0xf7), # GREEK SMALL LETTER PI
                0x0304 : byte(0xf8), # COMBINING MACRON
                0x00f7 : byte(0xfd), # DIVISION SIGN
                0x25a0 : byte(0xff)  # BLACK SQUARE
            }

            try:
                c = mapping[code_point]
            except KeyError:
                c = byte(0xff) # BLACK SQUARE

        # Special handling for 'x' followed by COMBINING MACRON
        if c == byte(0xf8):
            if len(ks0066u) == 0 or not ks0066u.endswith(byte(0x78)):
                c = byte(0xff) # BLACK SQUARE

            if len(ks0066u) > 0:
                ks0066u = ks0066u[:-1]

        ks0066u += c

    return ks0066u

##### STOP UNICODE TO KOS0006U ######


if __name__ == "__main__":

    ## CONNECTION
    ipcon = IPConnection() # Create IP connection

    mst = Master(mstUID, ipcon)   # Master Brick
    io = IO16(ioUID, ipcon)       # io16
    rp = RotaryPoti(rpUID, ipcon) # rotaryPoti
    lcd = LCD20x4(lcdUID, ipcon)  # lcd20x4

    ipcon.connect(HOST, PORT) # Connect to brickd
    ## END CONNECTION

    ## REGISTER CALLBACKS
    io.register_callback(io.CALLBACK_INTERRUPT, cb_interrupt)
    io.set_port_interrupt('b', 1 << 2) # port b2 to listen the door....

    lcd.register_callback(lcd.CALLBACK_BUTTON_PRESSED , cb_pressed )
    lcd.register_callback(lcd.CALLBACK_BUTTON_RELEASED, cb_released)
    ## END REGISTER CALLBACKS

    try:
        #c = Clock()
        #c.clearNum()
        #t = Thread(target=c.showTime) # can replace last none with ('MyArgument', 1)
        #t.start()
      
        t = Thread(target=stopApp) # this programm disables the connection to tinkerforge devices!
        t.start()
        
        #for i in range(10): # show 10 sleeps to demonstrate working threads
        #	t = Thread(target=timeout, args=(i,))
        #	t.start()
        
        # Turn backlight on
        lcd.backlight_on()

        tmp = str(mst.get_chip_temperature()/10)
        # Write some strings using the unicode_to_ks0066u function to map to the LCD charset
        lcd.write_line(0, 0, unicode_to_ks0066u('Stromstärke: 17µA'))
        lcd.write_line(1, 0, unicode_to_ks0066u('Temperatur:  ' + tmp + '°C'))

        # Write a string directly including characters from the LCD charset
        lcd.write_line(2, 0, b'Drehzahl:   750min\xe9')

        #print "hello!"
        # before join i can excute commands before Threads started
        t.join()
        # after join all commands wait for finished jobs

    except Exception as errtxt:
        print errtxt