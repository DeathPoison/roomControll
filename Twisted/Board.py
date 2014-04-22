#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time      import strftime # use for clock simulation - shows time!
from time      import sleep    # use for delay in loops - wait for n sec.!
from threading import Thread   # use to create a single threat for time

import sys   # for unicode_to_kos0006u
import types # for unicode_to_kos0006u

from tinkerforge.ip_connection        import IPConnection
from tinkerforge.brick_master         import Master
from tinkerforge.bricklet_io16        import IO16
from tinkerforge.bricklet_lcd_20x4    import LCD20x4
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_industrial_quad_relay import IndustrialQuadRelay


class Board():
    """
       This class handles the communication to my board!

        @author LimeBlack as David Crimi
        @require Hardware: 
            Master
            IO16
            LCD20x4
            IndustrialQuadRelay
    """

    def __init__(self, mst, io1, lcd, iqr, ilu, ipcon):

        self.ipcon = ipcon # Create IP connection

        self.mst = mst     # Master Brick
        self.io1 = io1     # io16
        self.lcd = lcd     # lcd20x4
        self.iqr = iqr     # Create device object
        self.ilu = ilu     # Create device object

        self.spyDoor   = False
        self.showState = False
        self.tmpLight  = False

        self.lcd.backlight_on()

        ## REGISTER CALLBACKS
        self.lcd.register_callback(self.lcd.CALLBACK_BUTTON_PRESSED , self.cb_pressed )
        self.lcd.register_callback(self.lcd.CALLBACK_BUTTON_RELEASED, self.cb_released)
        ## END REGISTER CALLBACKS

        ## Init noise
        self.io1.set_port_configuration('a', (1 << 0), 'o', True)        
        sleep(.1)
        self.io1.set_port_configuration('a', (1 << 0), 'o', False)         

    #### START LCD20x4 KEY CALLBACK ######

    def cb_pressed(self, i): 

        # Register pressed buttons - 0 = left, 1 = middle, 2 = right
        if i == 0 :
            #print "Pressed wrong button - button 0 left one!"
            # start & stop state on lcd
            if self.showState == True:
                self.showState = False
            else:
                self.showState = True
                self.state()
                print 'run bitch!'
                #t = Thread(target=self.state)
                #t.start()

            if self.spyDoor == True:
                self.spyDoor = False
            else:
                self.spyDoor = True
                t = Thread(target=self.door)
                t.start()                

        elif i == 1: 
            # Turn backlight on
            if self.lcd.is_backlight_on() == 1: 
                self.lcd.backlight_off()
            else:
                self.lcd.backlight_on()

        elif i == 2:
            pass

    def cb_released(self, i): # not in use!
        pass
        #print "Released: " + str(i)
        #if i == 0 :
            #print "released button left"
        #elif i == 1: 
            #print "released middle button"
        #elif i == 2:
            #print "released button on right"
    #### STOP LCD 20x4 KEY CALLBACK ######


    #### STATE ON LCD SCREEN ####
    def state(self):
        while self.showState:
            print 'state is updating...'
            tmp = str(self.mst.get_chip_temperature()/10)
            tmpAmb = str(self.ilu.get_illuminance()/10.0)
            # Write some strings using the unicode_to_ks0066u function to map to the LCD charset
            self.lcd.write_line(0, 0, self.unicode_to_ks0066u('Time: ' + strftime('%H:%M')))
            self.lcd.write_line(1, 0, self.unicode_to_ks0066u('Temperatur:  ' + tmp + '°C'))
            self.lcd.write_line(2, 0, self.unicode_to_ks0066u('Illuminace:  ' + tmpAmb + ' Lux'))
            sleep(1)
    #### END STATE ####




    ######## Commands ######################
    def status(self, parameter):
        if parameter == "door":
            binTmp = bin(self.io1.get_port('b')) # get value mask on port b binary
            #print binTmp
            tmpDoor = binTmp[9] # catch door bin 0b11111110 latest bit is the door
            if tmpDoor == '1':# OPEN
                return True # true = open
            if tmpDoor == '0':
                return False # closed
        if parameter == "temp":
            tmp = str(self.mst.get_chip_temperature()/10)
            return tmp
        if parameter == "beep":
            self.io1.set_port_configuration('a', (1 << 0), 'o', True)
            sleep(.5)
            self.io1.set_port_configuration('a', (1 << 0), 'o', False)
            return True
        if parameter == "light":
            if self.tmpLight:# OPEN
                self.tmpLight = False

                self.lcd.write_line(3, 0, "                    ") # 20x Blank to clear last line
                self.lcd.write_line(3, 0, self.unicode_to_ks0066u('Door: Open!'))

                self.iqr.set_value(0b0000000000001010) # turn on relay 1
                sleep(2)
                self.iqr.set_value(0b0000000000000000) # turn off remote
                sleep(2)
                return True

            else:
                self.tmpLight = True

                self.lcd.write_line(3, 0, "                    ") # 20x Blank to clear last line
                self.lcd.write_line(3, 0, self.unicode_to_ks0066u('Door: Closed... =)'))

                self.iqr.set_value(0b0000000000000110) # turn off relay 1
                sleep(2)
                self.iqr.set_value(0b0000000000000000) # turn off remote
                sleep(2)
                return False


    #### START DOOR SPY #####
    def door(self):

        tmpRAM = '1' # RAM save last value from door - to verify changes
        while self.spyDoor:
            sleep(2) # loop time!
            binTmp = bin(self.io1.get_port('b')) # get value mask on port b binary
            #print binTmp
            tmpDoor = binTmp[9] # catch door bin 0b11111110 latest bit is the door

            if tmpDoor != tmpRAM: # if notice changes

                if tmpDoor == '1':# OPEN
                    tmpRAM = tmpDoor

                    self.lcd.write_line(3, 0, "                    ") # 20x Blank to clear last line
                    self.lcd.write_line(3, 0, self.unicode_to_ks0066u('Door: Open!'))
                    
                    self.iqr.set_value(0b0000000000001010) # turn on relay 1
                    sleep(1)
                    self.iqr.set_value(0b0000000000000000) # turn off remote
                    sleep(1)

                elif tmpDoor == '0':# and value[7] == "0":
                    tmpRAM = tmpDoor

                    self.lcd.write_line(3, 0, "                    ") # 20x Blank to clear last line
                    self.lcd.write_line(3, 0, self.unicode_to_ks0066u('Door: Closed... =)'))

                    self.iqr.set_value(0b0000000000000110) # turn off relay 1
                    sleep(1)
                    self.iqr.set_value(0b0000000000000000) # turn off remote
                    sleep(1)  

    #### END DOOR SPY #####

    ########### SYSTEM COMMANDS :P ######
    @staticmethod # is static - self not nessesary! - accessable through the instance of this class
    def timeout(i):
        print("sleeping 5 sec from thread %d" % i)
        sleep(5)
        print("finished sleeping from thread %d" % i)

    def shutdown(self):
        raw_input('Press key to exit\n') # Use input() in Python 3
        #t.terminate() need to find a way stopping thread
        
        self.spyDoor = False        # turn all "apps" off
        self.showState = False      # means stop while loop
        self.lcd.backlight_off()    # and lcd screen off

        self.ipcon.disconnect()     # disconnect from tinkerforge
        quit()                      # close programm

    def quit(self):
        self.spyDoor = False        # turn all "apps" off
        self.showState = False      # means stop while loop
        self.lcd.backlight_off()    # and lcd screen off

        self.ipcon.disconnect()     # disconnect from tinkerforge
    #### END SYSTEM COMMANDS ############

    #### START UNICODE TO KOS0006U FOR LCD20x4 ######
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
    ##### STOP UNICODE TO KOS0006U ##################


if __name__ == "__main__":

    try:   

        ### Connection for Board
        PORT   = 4223
        BOARD_HOST   = "192.168.0.111"
        BOARD_mstUID = "62eUEf" # master brick
        BOARD_io1UID = "ghh"    # io16
        BOARD_lcdUID = "9ew"    # lcd screen 20x4
        BOARD_iqrUID = "eRN"    # industrial quad relay
        BOARD_iluUID = "i8U"    # industrial quad relay
        #### END BOARD CONNECTION

        # Connect to WLAN Controller
        ipcon = IPConnection() # Create IP connection

        mst = Master(BOARD_mstUID, ipcon)   # Master Brick
        io1 = IO16(BOARD_io1UID, ipcon)       # io16
        lcd1 = LCD20x4(BOARD_lcdUID, ipcon)  # lcd20x4
        iqr = IndustrialQuadRelay(BOARD_iqrUID, ipcon) # Create device object
        ilu = AmbientLight(BOARD_iluUID, ipcon) # Create device object

        ipcon.connect(BOARD_HOST, PORT) # Connect to brickd

        b = Board(mst, io1, lcd1, iqr, ilu, ipcon)

        #print b.status('temp')
        #print b.status('door')
        #print b.status('beep')
        #print b.status('light')
        #print b.status('light')
        #print b.status('light')


        t = Thread(target=b.shutdown) # this programm disables the connection to tinkerforge devices!
        t.start()

        # before join i can excute commands before Threads started
        t.join()
        # after join all commands wait for finished jobs
        
        print("SHUTDOWN Finished!")
        quit()

    except Exception as errtxt:
        print(errtxt)
