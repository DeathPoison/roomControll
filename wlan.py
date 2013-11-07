#!/usr/bin/env python
# -*- coding: utf-8 -*-  

HOST = "localhost"
PORT = 4223
lcdUID = "gFt" # Change to your UID
rpoUID = "g7Q"
lpoUID = "fwt"
jskUID = "hAP"

from time import sleep

import sys   # for unicode_to_kos0006u
import types # for unicode_to_kos0006u
from threading import Thread   # use to play around! - with style ;)

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_rotary_poti import RotaryPoti
from tinkerforge.bricklet_joystick import Joystick
from tinkerforge.bricklet_linear_poti import LinearPoti
from tinkerforge.bricklet_lcd_20x4 import LCD20x4

class Board():
    '''
       This class handles the communication to my board!

        @author LimeBlack as David Crimi
    '''

    def __init__(self):

        self.ipcon = IPConnection() # Create IP connection

        self.lcd = LCD20x4(lcdUID, self.ipcon) # Create device object LCD
        self.rpo = RotaryPoti(rpoUID, self.ipcon) # Create device object ROTARY POTI
        self.lpo = LinearPoti(lpoUID, self.ipcon) # Create device object LINEAR POTI
        self.jsk = Joystick(jskUID, self.ipcon) # Create device object JOYSTICK

        self.ipcon.connect(HOST, PORT) # Connect to brickd
        # Don't use device before ipcon is connected
   
        self.lcd.backlight_on() # Turn backlight on
        self.lcd.clear_display() # Clear Display

        ### Variables for PIN
        self.pinRun    = False              # Stop PIN loop!
        self.pinPos    = 0                  # Actually Position
        self.pinPW     = [ 150, 0, -150 ]   # Define Std Password PIN
        self.pinNo     = [ 0,   1,    2 ]   # Define PIN
        self.pinSt     = [ 0,   1,    2 ]   # Define PIN

        ## REGISTER CALLBACKS
        # Set Period for position callback to 0.05s (50ms)
        # Note: The position callback is only called every 50ms if the 
        #       position has changed since the last call!
        self.rpo.set_position_callback_period(50)
        self.lpo.set_position_callback_period(50)

        self.jsk.register_callback(self.jsk.CALLBACK_PRESSED,  self.cb_pressed )
        self.jsk.register_callback(self.jsk.CALLBACK_RELEASED, self.cb_released)

        self.rpo.register_callback(self.rpo.CALLBACK_POSITION, self.cb_position )
        self.lpo.register_callback(self.lpo.CALLBACK_POSITION, self.cb_positions)

        self.lcd.register_callback(self.lcd.CALLBACK_BUTTON_PRESSED , self.cb_pressedlcd )
        self.lcd.register_callback(self.lcd.CALLBACK_BUTTON_RELEASED, self.cb_releasedlcd)
        ## END REGISTER CALLBACKS

        ###### PLAYGROUD #######
        # here i can reach all devices!
        #self.lcd.write_line(0, 0, self.unicode_to_ks0066u('Trololololol '))
        ######

    # Callback functions for button status LCD20X4
    def cb_pressedlcd(self, i):
        # Register pressed buttons - 0 = left, 1 = middle, 2 = right
        if i == 0 :        
            # Turn backlight on
            self.lcd.backlight_off() if self.lcd.is_backlight_on() == 1 else self.lcd.backlight_on()

        elif i == 1: 
            sleep(0.1) # blanc ... 

        elif i == 2:
            sleep(0.1) # blanc ... 

        elif i == 3:
            #self.pinRun = True if self.pinRun == False else self.pinRun == False
            if self.pinRun == True:
               self.pinRun = False
            elif self.pinRun == False:
                self.pinRun = True
                
            sleep(0.1) # blanc ... 

    def cb_releasedlcd(self, i):
        # Register released buttons - 0 = left, 1 = middle, 2 = right, 3 = outer right
        if i == 0 :        
            sleep(0.1) # blanc ... 

        elif i == 1: 
            sleep(0.1) # blanc ... 

        elif i == 2:
            sleep(0.1) # blanc ... 

        elif i == 3:
            sleep(0.1) # blanc ... 

    # Callback function for pressed and released events JOYSTICK
    def cb_pressed(self):
        #self.pinRun = True if self.pinRun == False else self.pinRun == False
        self.pinSt[self.pinPos] = self.rpo.get_position()
        self.pinPos = self.pinPos + 1
        print "Stored " + str(self.rpo.get_position()) + " on Position " + str(self.pinPos - 1)

    def cb_released(self):
        sleep(0.1) # blanc ... 
        #print('JOYSTICK Released')

    # Callback function for position callback (parameter has range 0-100) LINEAR POTI
    def cb_positions(self, position):
        # Write position of Poti on LCD Screen
        self.lcd.write_line(0, 11, self.unicode_to_ks0066u('         '))
        self.lcd.write_line(0, 0, self.unicode_to_ks0066u('LPoti Pos : ' + str(position)))
        print('LINEAR POTI Position: ' + str(position))

    # Callbakc function for position events ROTARY POTI
    def cb_position(self, position):
        # Write position of Poti on LCD Screen
        self.lcd.write_line(1, 11, self.unicode_to_ks0066u('         '))
        self.lcd.write_line(1, 0, self.unicode_to_ks0066u('RPoti Pos : ' + str(position)))
        print("ROTARY POTI Position is: " + str(position))

    # Maps a Python string to the LCD charset
    def unicode_to_ks0066u(self, string):
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

    def stopApp(self):
        raw_input('Press key to exit\n') # Use input() in Python 3
        #t.terminate() need to find a way stopping thread
        self.ipcon.disconnect()
        quit()

if __name__ == "__main__":

    try:
        run = Board()

        #t = Thread(target=run.pin) # this programm disables the connection to tinkerforge devices!
        #t.start()            
        
        t = Thread(target=run.stopApp) # this programm disables the connection to tinkerforge devices!
        t.start()

        run.pinRun = True
        while run.pinRun == True:
            tmppos = run.rpo.get_position()
            #Write position of Poti on LCD Screen
            run.lcd.write_line(2, 11, run.unicode_to_ks0066u('          '))
            run.lcd.write_line(2, 0, run.unicode_to_ks0066u('Pin Code/X: ' + str(tmppos)))

            ### DEBUG ###
            print("  ")
            print("pin0   : " + str(run.pinNo[0]))
            print("pin1   : " + str(run.pinNo[1]))
            print("pin2   : " + str(run.pinNo[2]))
            print("pinSt0   : " + str(run.pinSt[0]))
            print("pinSt1   : " + str(run.pinSt[1]))
            print("pinSt2   : " + str(run.pinSt[2]))
            print("pinPW : " + str(run.pinPW))
            print("pinPOS: " + str(run.pinPos))

            if run.pinSt[0] == run.pinPW[0] and run.pinSt[1] == run.pinPW[1] and run.pinSt[2] == run.pinPW[2]:
                run.lcd.write_line(3, 0, run.unicode_to_ks0066u('Successfully logged in!'))
                run.pinRun = False
            elif run.pinPos == 3:
                run.pinRun = False
                run.lcd.clear_display()
                run.lcd.write_line(0, 0, run.unicode_to_ks0066u('You will die in 3...'))
                sleep(1)
                run.lcd.write_line(1, 0, run.unicode_to_ks0066u('You will die in 2...'))
                sleep(1)
                run.lcd.write_line(2, 0, run.unicode_to_ks0066u('You will die in 1...'))
                sleep(1)
                run.lcd.write_line(3, 0, run.unicode_to_ks0066u('You will die in 0...'))
                run.lcd.write_line(0, 0, run.unicode_to_ks0066u('.----.   .-.  .----.'))
                run.lcd.write_line(1, 0, run.unicode_to_ks0066u('| {}  \  | |  | {_  '))
                run.lcd.write_line(2, 0, run.unicode_to_ks0066u('|     /  | |  | {__ '))
                run.lcd.write_line(3, 0, run.unicode_to_ks0066u('`----\'   `-\'  `----\''))
                sleep(3)
                run.lcd.backlight_off() # Turn backlight on
                run.ipcon.disconnect()
                quit()

            sleep(1)

        t.join()
        pass

    except Exception as e:
        print e
        