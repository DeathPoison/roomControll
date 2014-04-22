#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import strftime      # use for clock simulation - shows time!
from time import sleep         # use for delay in loops - wait for n sec.!
from threading import Thread   # use to create a single threat for time

import sys    # for unicode_to_kos0006u
import types  # for unicode_to_kos0006u

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_joystick import Joystick
from tinkerforge.bricklet_lcd_20x4 import LCD20x4

# from tinkerforge.bricklet_rotary_poti import RotaryPoti
# from tinkerforge.bricklet_linear_poti import LinearPoti


class Menu():
    def __init__(self, jsk, lcd, ipcon, board):

        self.jsk = jsk           # set Hardware
        self.lcd = lcd           # set Hardware
        self.ipcon = ipcon       # set Hardware
        self.board = board       # use the board

        self.exit = False        # to stop main loop
        self.executable = False  # Menu contains exec. Elements -> default: no
        self.lcdRows = 4         # max LCD-Rows

        self.page = 0            # default page
        self.tmp_pos = 1         # default value to clear last position
        self.borderA = '| - '    # starting border - in middle take menu point!
        self.borderB = ' |'      # ending   border

        self.content = {        # My Menu
            'Main': {                                              # Menu always is a dict.
                '1 Tinkerforge': {'2 Door':   ['Status',
                                               'Toggle Light']},   # beginning with key as menu title and a list as value

                # '2 Trash':       { '1 BEEP':   ['Start',
                #                                'Stop',
                #                                '1sec Beep']},    # witch are subtitles or functions

                '2 Trash':       {'1 BEEP':   'Beep'},     # witch are subtitles or functions

                '3 Status':      {'1 Master': ['Temp',
                                               'Voltage',
                                               'Light Lvl',
                                               'Ext. Voltage']},  # !! Menus in menus are not allowed this time!

                '4 Version':                   ['Version: 0.3b',
                                                'Created by',
                                                'LimeBlack'],
            }
        }

        self.posY = 0                                   # used for selection in a menu
        self.posX = self.content.keys()[0]              # used for return/back in menu - now holds Title of Menu - 'Main'

        self.content[self.posX].keys().sort()           # sort keys to get rigth order

        self.header = self.padHeader(self.content.keys()[0])

        self.getPages(self.content[self.posX].keys())   # get nesessary pages
        self.setPage(0)                                 # display first page

        self.lcd.backlight_on()                         # Turn of LCD Backlight

        # # REGISTER CALLBACKS
        self.jsk.register_callback(
            self.jsk.CALLBACK_PRESSED,  self.cb_pressedjsk)
        self.jsk.register_callback(
            self.jsk.CALLBACK_RELEASED, self.cb_releasedjsk)

        self.jsk.set_debounce_period(400)                                # Get threshold callbacks with a debounce time of 0.2 seconds (200ms)
        self.jsk.register_callback(                                      # Register threshold reached callback to function cb_reached
            self.jsk.CALLBACK_POSITION_REACHED, self.cb_reachedjsk)
        self.jsk.set_position_callback_threshold('o', -99, 99, -99, 99)  # Configure threshold for 'x and y value outside of [-99..99]'

        self.lcd.register_callback(self.lcd.CALLBACK_BUTTON_PRESSED,  self.cb_pressedlcd)
        self.lcd.register_callback(self.lcd.CALLBACK_BUTTON_RELEASED, self.cb_releasedlcd)
        # # END REGISTER CALLBACKS

    # ## Little functions - like Menu-tools ####
    def display(self):              # display current self.screen on lcd
        self.lcd.write_line(0, 0, self.unicode_to_ks0066u(self.header))
        for index, x in enumerate(self.screen):
            self.lcd.write_line(index+1, 0, self.unicode_to_ks0066u(x))
            # print index+1, x
        return True

    def getPages(self, someList):                    # Get needed pages - save in self.pages
        lenX = len(someList) / (self.lcdRows - 1)    # -1 for header
        if len(someList) % (self.lcdRows - 1) >= 1:  # if value is odd we add 1 for rest entrys
            self.pages = lenX + 1
        else:
            self.pages = lenX
        return self.pages

    def setCursor(self, pos):       # set cursor on LCD-Screen   - - - ONLY DRAW + ON GIVEN(X) LCD ROW!
        self.lcd.write_line(self.tmp_pos, 2, self.unicode_to_ks0066u('-'))
        # self.lcd.write_line(2, 2, self.unicode_to_ks0066u('-'))
        # self.lcd.write_line(3, 2, self.unicode_to_ks0066u('-'))

        if pos in range(0, 4):
            self.lcd.write_line(pos, 2, self.unicode_to_ks0066u('+'))

            self.tmp_pos = pos  # save pos for next step
            pass
        else:
            return "Position not on Sceen!"

    # ## REALLY IMPORTANT FUNCTION
    def pushListScreen(self, anyList):
        if type(anyList) == list:
            for row in range(0, self.lcdRows-1):                # for each row on lcd screen do:
                y = self.page * (self.lcdRows - 1) + row
                if y in range(0, len(anyList)):
                    tmpValue = anyList
                    tmpValue.sort()
                    self.screen.append(self.pad(tmpValue[y]))   # append menu entry to self.screen
                else:
                    self.screen.append(self.pad('empty'))       # append empty if no menu entry fount 
            return self.screen
        else:
            return 'not a list!'

    def setPage(self, thisPage):     # set a new Page - fill self.screen with current menu !
        # Need to check posY !

        if type(self.posX) == str:  # we are on menu lvl 1 - cant contain executable elements
            # check page and show items of menu[poxY]
            if thisPage in range(0, self.pages):          # thisPage is a valid page
                self.page = thisPage
                self.screen = []

                self.executable = False
                self.pushListScreen(self.content[self.posX].keys())

                self.display()                       # display screen
                return True
            else:
                return False

        if type(self.posX) == list:                     # we are on menu lvl 2
            if len(self.posX) == 2:
                if thisPage in range(0, self.pages):    # page is valid
                    self.page = thisPage
                    self.screen = []
                    # print 'here is what i search!: ' + str(self.content[self.posX[0]][self.posX[1]])
                    if type(self.content[self.posX[0]][self.posX[1]]) == dict:
                        self.executable = False
                        self.pushListScreen(self.content[self.posX[0]][self.posX[1]].keys())

                        self.display()                       # display screen
                        return True

                    elif type(self.content[self.posX[0]][self.posX[1]]) == list:
                        self.executable = True
                        self.pushListScreen(self.content[self.posX[0]][self.posX[1]])

                        self.display()                       # display screen
                        return True
                else:
                    return False

            elif len(self.posX) == 3:                   # we are on menu lvl 3
                if thisPage in range(0, self.pages):
                    # page is valid
                    self.page = thisPage
                    self.screen = []
                    # print 'here is what i search!: ' + str(self.content[self.posX[0]][self.posX[1]][self.posX[2]])
                    if type(self.content[self.posX[0]][self.posX[1]][self.posX[2]]) == dict:
                        self.executable = False
                        self.pushListScreen(self.content[self.posX[0]][self.posX[1]][self.posX[2]].keys())

                        self.display()                       # display screen
                        return True

                    elif type(self.content[self.posX[0]][self.posX[1]][self.posX[2]]) == list:
                        self.executable = True
                        self.pushListScreen(self.content[self.posX[0]][self.posX[1]][self.posX[2]])

                        self.display()                       # display screen
                        return True
                else:
                    return False

            elif len(self.posX) == 4:
                print 'Thats pretty deep bitch!'
                pass

            # if len(posSub) == 3 show items of menu[poxY[0]][poxY[1]][poxY[2]]
            # if len(posSub) >= 4 print "such deep menus are not allowed!"
    # ## END Little functions - like Menu-tools ####

    # ## MAIN FUNCTION - WITH JOYSTICK I MOVE IN MENU
    def cb_reachedjsk(self, x, y):  # Callback for x and y position outside of [-99..99]

        if y == 100:                # ## UP   # Y is easy any move in list i already have! - only move coursor up/down

            self.posY -= 1
            if self.posY in range(1, self.lcdRows):  # if posY is on screen
                self.setCursor(self.posY)
            else:
                self.posY = self.lcdRows-1
                self.page -= 1

                if self.page >= self.pages or self.page < 0:
                    # if self.page in range(0,self.pages):
                    self.page = self.pages-1
                    self.setPage(self.page)
                    self.setCursor(self.posY)
                else:
                    self.setPage(self.page)
                    self.setCursor(self.posY)

        elif y == -100:       # ## DOWN

            self.posY += 1
            if self.posY in range(1, self.lcdRows):  # if posY is on screen
                self.setCursor(self.posY)
            elif self.posY >= 0:                     # or outside of screen
                self.posY = 1
                self.page += 1
                if self.page >= self.pages:
                    self.page = 0
                    self.setPage(self.page)
                    self.setCursor(self.posY)
                else:
                    self.setPage(self.page)
                    self.setCursor(self.posY)

        if x == 100:        # ## RIGHT # X is much more dif. cause i need to search and save current position to generate new lists i can move in

            if type(self.posX) == str:
                tmpCOntent = self.content[self.posX].keys()
                tmpCOntent.sort()

                for index, item in enumerate(tmpCOntent):
                    if index == (self.page * (self.lcdRows-1)) + self.posY-1:   # page + lcdRows + posY = actually pos in list
                        # print 'item I search is: ' + str(item)
                        self.header = self.padHeader(str(item))                 # save new header - choosen menu entry!

                        # # need to check if NEW menu is a dict(another menu) of a list(functions)
                        if type(self.content[self.posX][str(item)]) == dict:
                            self.getPages(self.content[self.posX][str(item)].keys())    # get new neccessary pages

                        elif type(self.content[self.posX][str(item)]) == list:
                            self.getPages(self.content[self.posX][str(item)])

                        self.posX = [self.posX]       # convert posX in list
                        self.posX.append(str(item))

                        self.posY = 1                 # reset posY
                        self.setCursor(self.posY)

                        self.page = 0
                        self.setPage(0)     # push page content to screen

            elif type(self.posX) == list:

                if len(self.posX) >= 4:
                    print 'thats to deep!'
                    pass

                elif len(self.posX) == 2:   # menu lvl 2
                    tmpConent = self.content[self.posX[0]][self.posX[1]]    # get menu and...
                    self.enterNextLvl(tmpConent)                            # get into it!

                elif len(self.posX) == 3:   # menu lvl 3
                    tmpConent = self.content[self.posX[0]][self.posX[1]][self.posX[2]]
                    self.enterNextLvl(tmpConent)

        elif x == -100:       # ## LEFT
            if type(self.posX) == str:
                pass

            elif type(self.posX) == list:
                tmpContent = self.content[self.posX[0]]

                if len(self.posX) >= 4:
                    print 'thats to deep!'
                    pass

                elif len(self.posX) == 2:                   # menu lvl 2
                    self.header = self.padHeader(self.posX[0])           # save new header - choosen menu entry!

                    if type(tmpContent) == dict:            # # need to check if NEW menu is a dict(another menu) of a list(functions)
                        self.getPages(tmpContent.keys())    # get new neccessary pages

                    elif type(tmpContent[self.posX[0]]) == list:
                        self.getPages(tmpContent[self.posX[0]])

                    self.posX = self.posX[0]                # get menu and...

                    self.posY = 1                           # reset posY
                    self.setCursor(self.posY)

                    self.page = 0
                    self.setPage(0)                         # push page content to screen        # get into it!

                elif len(self.posX) == 3:                   # menu lvl 3
                    self.header = self.padHeader(self.posX[1])           # save new header - choosen menu entry!

                    if type(tmpContent[self.posX[1]]) == dict:           # # need to check if NEW menu is a dict(another menu) of a list(functions)
                        self.getPages(tmpContent[self.posX[1]].keys())   # get new neccessary pages

                    elif type(tmpContent[self.posX[1]]) == list:
                        self.getPages(tmpContent[self.posX[1]])

                    self.posX = [self.posX[0], self.posX[1]]

                    self.posY = 1                 # reset posY
                    self.setCursor(self.posY)

                    self.page = 0
                    self.setPage(0)     # push page content to screen

    def enterNextLvl(self, menuParticle):

        if type(menuParticle) == str:
            return self.startCommand(str(menuParticle))

        if type(menuParticle) == list:
            if self.executable:
                for index, item in enumerate(menuParticle):

                    if index == (self.page * (self.lcdRows-1)) + self.posY-1:   # page + lcdRows + posY = actually pos in list
                        print 'EXECUTABLE IS: ' + str(item)
                        return self.startCommand(str(item))
            else:
                return 'should not happen!'

        elif type(menuParticle) == dict:
            tmpCOntent = menuParticle.keys()
            tmpCOntent.sort()

            for index, item in enumerate(tmpCOntent):

                if index == (self.page * (self.lcdRows-1)) + self.posY-1:  # page + lcdRows + posY = actually pos in list
                    # print 'item I search is: ' + str(item)
                    self.header = self.padHeader(str(item))           # save new header - choosen menu entry!

                    if type(menuParticle[str(item)]) == dict:         # # need to check if NEW menu is a dict(another menu) of a list(functions)
                        self.getPages(menuParticle[str(item)].keys())  # get new neccessary pages

                    elif type(menuParticle[str(item)]) == list:
                        self.getPages(menuParticle[str(item)])

                    self.posX.append(str(item))

                    self.posY = 1                 # reset posY
                    self.setCursor(self.posY)

                    self.page = 0
                    self.setPage(0)     # push page content to screen
                    return

    def startCommand(self, command):
        if type(command) == str:
            if command == "Toggle Light":
                print self.board.status('light')
                return
            if command == "Status":
                print self.board.status('door')
                return
            if command == "Beep":
                print self.board.status('beep')
                return
            if command == "Temp":
                print self.board.status('temp')
                return
            #if command == "Voltage":
            #if command == "Light Lvl":
            #    return self.board.status('light')

            return 'not implemented yet!'

        else:
            return False

    ### STOP MAIN FUNCTION

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
    ##### STOP UNICODE TO KOS0006U ######


    ##### CALLBACKS ###########
    def cb_pressedlcd(self, i): # Callback functions for button status LCD20X4
        # Register pressed buttons - 0 = left, 1 = middle, 2 = right
        if i == 0 :
            # Turn backlight on
            self.lcd.backlight_off() if self.lcd.is_backlight_on() else self.lcd.backlight_on()

        elif i == 1: 
            sleep(0.1) # blanc ... 

        elif i == 2:
            sleep(0.1) # blanc ... 

        elif i == 3:
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

    def cb_pressedjsk(self):  # Callback function for pressed and released events JOYSTICK
        #pinRun = True if pinRun == False else pinRun == False
        #pinSt[pinPos] = rpo.get_position()
        #pinPos = pinPos + 1
        #print "Stored " + str(rpo.get_position()) + " on Position " + str(pinPos - 1)
        pass

    def cb_releasedjsk(self):
        sleep(0.1) # blanc ... 
        #print('JOYSTICK Released')    
    ##### STOP CALLBACKS ######


    ##### Tools ######
    def shutdown(self):
        sleep(2)
        raw_input('Press key to exit\n') # Use input() in Python 3
        #self.lcd.write_line(0, 0, self.unicode_to_ks0066u('Shutdown...           '))
        #self.lcd.write_line(1, 0, self.unicode_to_ks0066u('Shutdown...           '))
        #self.lcd.write_line(2, 0, self.unicode_to_ks0066u('Shutdown...           '))
        self.lcd.write_line(3, 0, self.unicode_to_ks0066u('Shutdown...           '))
        print "SHUTDOWN initiated"
        self.lcd.backlight_off() # turn off backlight
        self.exit = True         # stop run loop
        self.ipcon.disconnect()
        quit()                   # quit python env?

    def quit(self):
        self.lcd.write_line(3, 0, self.unicode_to_ks0066u('Shutdown...           '))
        print "SHUTDOWN initiated"
        self.lcd.backlight_off() # turn off backlight
        self.exit = True         # stop run loop
        self.ipcon.disconnect()

    def pad(self, inputString):   # pad a string up to 20 chars
        a = 13 - len(inputString)
        tmp = self.borderA + inputString + " " + (a*"-") + self.borderB
        if len(tmp) <= 20:
            return tmp
        else: 
            return "Something goes wrong"

    def padHeader(self, inpStr):
        strLen = len(inpStr)
        strOdd = strLen % 2
        countSlash = (((16 - strLen) /2) *'-')
        
        if strLen >= 16:  return "|- Input to Long! -|"
        elif strOdd == 1:
            goal = '|' + countSlash + ' ' + inpStr + ' ' + countSlash + '-|'
            return goal
        else:
            goal = '|' + countSlash + ' ' + inpStr + ' ' + countSlash + '|'
            return goal
    ####### END Tools #########

if __name__ == "__main__": # Only used on direct access!

    try:

        try:
            from Board import Board as B
            from tinkerforge.brick_master         import Master
            from tinkerforge.bricklet_io16        import IO16
            from tinkerforge.bricklet_ambient_light import AmbientLight
            from tinkerforge.bricklet_industrial_quad_relay import IndustrialQuadRelay
        except ImportError as err:
            print err


        ### Connection for Menu
        WLAN_PORT   = 4223
        WLAN_HOST = "127.0.0.1"#"192.168.0.150" # Manually Set IP of Controller Board
        WLAN_lcdUID = "gFt" # LCD Screen
        WLAN_jskUID = "hAP" # Joystick
        ### END MENU CONNECTION

        ### Connection for Board
        BOARD_HOST   = "192.168.0.111"
        BOARD_mstUID = "62eUEf" # master brick
        BOARD_io1UID = "ghh"    # io16
        BOARD_lcdUID = "9ew"    # lcd screen 20x4
        BOARD_iqrUID = "eRN"    # industrial quad relay
        BOARD_iluUID = "i8U"    # Ambient Light
        #### END BOARD CONNECTION

        BOARD_ipcon = IPConnection() # Create IP connection

        mst = Master(BOARD_mstUID, BOARD_ipcon)   # Master Brick
        io1 = IO16(BOARD_io1UID, BOARD_ipcon)       # io16
        lcd1 = LCD20x4(BOARD_lcdUID, BOARD_ipcon)  # lcd20x4
        iqr = IndustrialQuadRelay(BOARD_iqrUID, BOARD_ipcon) # Create device object
        ilu = AmbientLight(BOARD_iqrUID, BOARD_ipcon) # Create device object

        BOARD_ipcon.connect(BOARD_HOST, WLAN_PORT) # Connect to brickd

        # create Board instance
        BB = B(mst, io1, lcd1, iqr, ilu, BOARD_ipcon)
        print "started board"
        print BB.status('door')

        # Connect to WLAN Controller
        WLAN_ipcon = IPConnection() # Create IP connection
        lcd = LCD20x4(WLAN_lcdUID, WLAN_ipcon) # Create device object LCD
        jsk = Joystick(WLAN_jskUID, WLAN_ipcon) # Create device object JOYSTICK
        
        # Don't use device before ipcon is connected
        WLAN_ipcon.connect(WLAN_HOST, WLAN_PORT) # Connect to brickd
      
        n = Menu(jsk, lcd, WLAN_ipcon, BB) # yeah dont need thread ;)
        print n.board.status('door')
        print "started menu"

        n.shutdown() # close application  
        print "SHUTDOWN Finished!" 
        quit()

    except Exception as errtxt:
        print errtxt
