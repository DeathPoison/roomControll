#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Important Imports
try:
    from tinkerforge.ip_connection import IPConnection

    from time import strftime       # use for bash time
    from time import sleep          # use for delay in loops - wait for n sec.!
    from threading import Thread    # use to create a single threat for time

    import sys                      # for unicode_to_kos0006u
    import types                    # for unicode_to_kos0006u

    # Imports for WebSockets!
    # from twisted.internet import reactor, ssl
    # from twisted.python import log
    # from twisted.web.server import Site
    # from twisted.web.static import File

    # from autobahn.twisted.websocket import WebSocketServerProtocol
    # from autobahn.twisted.websocket import WebSocketServerFactory
    # from autobahn.twisted.websocket import listenWS

    # #### Own Libraries #### #
    try:
        from l_bcolors import bcolors as bc
        from l_cli import TinkerCli
        # from l_cmdline import cmdline # outdated

    except ImportError as erroror:
        print erroror
except ImportError as err:
    print err


class ForgeTinker():
    """Probably the handler for reverse(ForgeTinker) """

    def __init__(self):

        self.HOST = "localhost"  # "192.168.0.111"  # "localhost"
        self.PORT = 4223
        self.debug = False

        self.deviceList = []

        self.user = "GuestUser"
        self.mode = 'home'

        self.haveEther = False  # need to saved through multiple calls
        self.haveWifi = False  # need to saved through multiple calls

        self.spyDoor = False
        self.openDoor = False
        self.showLight = False
        self.showState = False

        # Create connection and connect to brickd
        self.ipcon = IPConnection()
        self.ipcon.connect(self.HOST, self.PORT)

        # Register Enumerate Callback
        self.ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, self.cb_enumerate)

        self.connection_dict = {
            # '11': self.BrickDC(),
            '13':  self.BrickMaster,  # master brick
            # '14': self.BrickServo(),
            # '15': self.BrickStepper(),
            '21':  self.BrickletAmbientLight,  # ambient light
            # '25': self.BrickletDistanceIR(),
            '27':  self.BrickletHumidity,  # humidity
            '28':  self.BrickletIO16,  # io16
            '210': self.BrickletJoystick,  # joystick
            '212': self.BrickletLCD20x4,  # lcd display 20x4
            '213': self.BrickletLinearPoti,  # linear poti
            '215': self.BrickletRotaryPoti,  # rotary poti
            '216': self.BrickletTemperature,  # temperatur
            '217': self.BrickletTemperatureIR,  # temperatur ir
            '221': self.BrickletBarometer,  # barometer
            '225': self.BrickletIndustrialQuadRelay,  # industrial quad relay
        }

        # Trigger Enumerate
        self.ipcon.enumerate()

        # print 'Wait 1 second for Devices!'
        sleep(1)

        if len(self.deviceList) <= 1:
            print bc.Red + 'No Device Found!' + bc.end

        #if not self.showState:
        #    self.toggleState()
        #if not self.spyDoor:
        #    self.toggleDoor()
        #if not self.showLight:
        #    self.toggleLight()

        #    deviceType = str(device).split('.')[1]
        #    if deviceType == 'bricklet_ambient_light':
        # bash()

    # ###############################################
    # ################################################
    # ################# run / quit ###################
    # ###############################################
    # ################################################

    def run(self, user, ownInstance):
        TinkerCli().cmdloop(user, ownInstance)

    def quit(self):
        self.spyDoor = False
        self.showState = False
        print bc.Red + 'Disconnect from Tinkerforge!' + bc.end
        print bc.Red + 'This takes exactly 1.5 Seconds!' + bc.end
        sleep(1.5)   # wait for loops to finish
        self.ipcon.disconnect()

    # ###############################################
    # ################################################
    # ################# CONNECTION ###################
    # ###############################################
    # ################################################

    def BrickMaster(self, action, uid, cUid=None, value=None):
        # ~ init - connect to device!
        if action == 'connect':
            try:
                from tinkerforge.brick_master import Master
            except ImportError as err:
                print err
            else:
                self.removeUID(uid)

                mst = Master(uid, self.ipcon)    # Master Brick

                mststr = str(mst).split()        # get device type
                mstname = mststr[0].split('.')
                devtype = mstname[2]

                self.deviceList.append({
                    'name': devtype,
                    'instance': mst,
                    'uid': uid,
                    'cuid': cUid,
                })
                return True

        # ~ list - get functions of device!
        if action == 'list':
            getList = [{
                'name': 'Version',
                'command': 'get_api_version',
            }, {
                'name': 'Identity',
                'command': 'get_identity',
            }, {
                'name': 'Temperatur',
                'command': 'get_chip_temperature',
            }, {
                'name': 'Voltage',
                'command': 'get_stack_voltage',
            }, {
                'name': 'USB Voltage',
                'command': 'get_usb_voltage',
            }, {
                'name': 'Current',
                'command': 'get_stack_current',
            }, {
                'name': 'Ethernet',
                'command': 'is_ethernet_present',
            }, {
                'name': 'Ethernet Status',
                'command': 'get_ethernet_status',
            }, {
                'name': 'Wifi',
                'command': 'is_wifi_present',
            }, {
                'name': 'Wifi Status',
                'command': 'get_wifi_status',
            }]

            setList = {
                'reset': 'reset'
            }

            # callbacks
                # callback_stack_current
                # callback_stack_voltage
                # callback_usb_current

                # debounce_period
                # threshold of callbacks

            masterFunctions = {'get': getList, 'set': setList}

            return masterFunctions

    def BrickletAmbientLight(self, action, uid, cUid=None, value=None):    # Device = Ambient Light Bricklet
        # ~ init - connect to device!
        if action == 'connect':
            try:
                from tinkerforge.bricklet_ambient_light import AmbientLight
            except ImportError as err:
                print err
                # if str(uid) == 'i8U': #    print 'Ambient Light Bricklet found...'
            else:  # Create device object
                self.removeUID(uid)

                amb = AmbientLight(uid, self.ipcon)

                ambstr = str(amb).split()        # get device type
                ambname = ambstr[0].split('.')
                devtype = ambname[2]

                self.deviceList.append({
                    'name': devtype,
                    'instance': amb,
                    'uid': uid,
                    'cuid': cUid
                })
                return

        # ~ list - get functions of device!
        if action == 'list':
            getList = [{
                'name': 'Version',
                'command': 'get_api_version',
            }, {
                'name': 'Identity',
                'command': 'get_identity',
            }, {
                'name': 'Illuminance',
                'command': 'get_illuminance',
            }, {
                'name': 'Analog',
                'command': 'get_analog_value',
            }]

            setList = {'reset': 'reset'}

            liste = {'get': getList, 'set': setList}

            return liste

    def BrickletLinearPoti(self, action, uid, cUid=None, value=None):    # Device = IO-16 Bricklet
        if action == 'connect':
            try:
                from tinkerforge.bricklet_linear_poti import LinearPoti
            except ImportError as err:
                print err
                # if str(uid) == 'ghh':
                #    print 'IO-16 Bricklet found...'
            else:
                self.removeUID(uid)

                lipo = LinearPoti(uid, self.ipcon)         # io16

                lipostr = str(lipo).split()        # get device type
                liponame = lipostr[0].split('.')
                devtype = liponame[2]

                self.deviceList.append({
                    'name': devtype,
                    'instance': lipo,
                    'uid': uid,
                    'cuid': cUid
                })
                return

        # ~ list - get functions of device!
        if action == 'list':
            getList = [{
                'name': 'Version',
                'command': 'get_api_version',
            }, {
                'name': 'Identity',
                'command': 'get_identity',
            }, {
                'name': 'Position',
                'command': 'get_position',
            }, {
                'name': 'Analog',
                'command': 'get_analog_value',
            }]

            setList = {'reset': 'reset'}

            liste = {'get': getList, 'set': setList}

            return liste

    def BrickletIO16(self, action, uid, cUid=None, value=None):    # Device = IO-16 Bricklet
        if action == 'connect':
            try:
                from tinkerforge.bricklet_io16 import IO16
            except ImportError as err:
                print err
                # if str(uid) == 'ghh':
                #    print 'IO-16 Bricklet found...'
            else:
                self.removeUID(uid)
                io16 = IO16(uid, self.ipcon)         # io16

                io16str = str(io16).split()        # get device type
                io16name = io16str[0].split('.')
                devtype = io16name[2]

                self.deviceList.append({
                    'name': devtype,
                    'instance': io16,
                    'uid': uid,
                    'cuid': cUid
                })
                return

        # ~ list - get functions of device!
        if action == 'list':
            getList = [{
                'name': 'Version',
                'command': 'get_api_version',
            }, {
                'name': 'Identity',
                'command': 'get_identity',
            }, {
                'name': 'Port',
                'command': 'get_port',   # need arguments ( a or b )
            }, {
                'name': 'Analog',
                'command': 'get_analog_value',
            }]

            setList = {'reset': 'reset'}

            liste = {'get': getList, 'set': setList}

            return liste

    def BrickletBarometer(self, action, uid, cUid=None, value=None):    # Device = IO-16 Bricklet
        if action == 'connect':
            try:
                from tinkerforge.bricklet_barometer import Barometer
            except ImportError as err:
                print err
                # if str(uid) == 'ghh':
                #    print 'IO-16 Bricklet found...'
            else:
                self.removeUID(uid)
                baro = Barometer(uid, self.ipcon)         # io16

                barostr = str(baro).split()        # get device type
                baroname = barostr[0].split('.')
                devtype = baroname[2]

                self.deviceList.append({
                    'name': devtype,
                    'instance': baro,
                    'uid': uid,
                    'cuid': cUid
                })
                return

        # ~ list - get functions of device!
        if action == 'list':
            getList = [{
                'name': 'Version',
                'command': 'get_api_version',
            }, {
                'name': 'Identity',
                'command': 'get_identity',
            }, {
                'name': 'Air Pressure',
                'command': 'get_air_pressure',  # need arguments ( a or b )
            }, {
                'name': 'Altitude',
                'command': 'get_altitude',
            }, {
                'name': 'Reference Air Pressure',
                'command': 'get_reference_air_pressure',   # default: 1013,25mbar
            }, {
                'name': 'Temperature',
                'command': 'get_chip_temperature',
            }, {
                'name': 'Averaging',
                'command': 'get_averaging',
            }]

            setList = {'reset': 'reset'}

            liste = {'get': getList, 'set': setList}

            return liste

    def BrickletHumidity(self, action, uid, cUid=None, value=None):    # Device = IO-16 Bricklet
        if action == 'connect':
            try:
                from tinkerforge.bricklet_humidity import Humidity
            except ImportError as err:
                print err
                # if str(uid) == 'ghh':
                #    print 'IO-16 Bricklet found...'
            else:
                self.removeUID(uid)
                hum = Humidity(uid, self.ipcon)         # io16

                humstr = str(hum).split()        # get device type
                humname = humstr[0].split('.')
                devtype = humname[2]

                self.deviceList.append({
                    'name': devtype,
                    'instance': hum,
                    'uid': uid,
                    'cuid': cUid
                })
                return

        # ~ list - get functions of device!
        if action == 'list':
            getList = [{
                'name': 'Version',
                'command': 'get_api_version',
            }, {
                'name': 'Identity',
                'command': 'get_identity',
            }, {
                'name': 'Humidity',
                'command': 'get_humidity',  # need arguments ( a or b )
            }, {
                'name': 'Analog',
                'command': 'get_analog_value',
            }]

            setList = {'reset': 'reset'}

            liste = {'get': getList, 'set': setList}

            return liste

    def BrickletTemperature(self, action, uid, cUid=None, value=None):    # Device = IO-16 Bricklet
        if action == 'connect':
            try:
                from tinkerforge.bricklet_temperature import Temperature
            except ImportError as err:
                print err
                # if str(uid) == 'ghh':
                #    print 'IO-16 Bricklet found...'
            else:
                self.removeUID(uid)
                tem = Temperature(uid, self.ipcon)   # Create device object

                temstr = str(tem).split()        # get device type
                temname = temstr[0].split('.')
                devtype = temname[2]

                self.deviceList.append({
                    'name': devtype,
                    'instance': tem,
                    'uid': uid,
                    'cuid': cUid
                })
                return

        # ~ list - get functions of device!
        if action == 'list':
            getList = [{
                'name': 'Version',
                'command': 'get_api_version',
            }, {
                'name': 'Identity',
                'command': 'get_identity',
            }, {
                'name': 'Temperatur',
                'command': 'get_temperature',
            }, {
                'name': 'I2C Mode',
                'command': 'get_i2c_mode',  # 0 = Fast (400kHz) | 1 = Slow (100kHz)
            }]

            setList = {'reset': 'reset'}

            liste = {'get': getList, 'set': setList}

            return liste

    def BrickletTemperatureIR(self, action, uid, cUid=None, value=None):    # Device = IO-16 Bricklet
        if action == 'connect':
            try:
                from tinkerforge.bricklet_temperature_ir import TemperatureIR
            except ImportError as err:
                print err
                # if str(uid) == 'ghh':
                #    print 'IO-16 Bricklet found...'
            else:
                self.removeUID(uid)
                tir = TemperatureIR(uid, self.ipcon)

                tirstr = str(tir).split()        # get device type
                tirname = tirstr[0].split('.')
                devtype = tirname[2]

                self.deviceList.append({
                    'name': devtype,
                    'instance': tir,
                    'uid': uid,
                    'cuid': cUid
                })
                return

        # ~ list - get functions of device!
        if action == 'list':
            getList = [{
                'name': 'Version',
                'command': 'get_api_version',
            }, {
                'name': 'Identity',
                'command': 'get_identity',
            }, {
                'name': 'Ambient Temperatur',
                'command': 'get_ambient_temperature',
            }, {
                'name': 'Object Temperatur',
                'command': 'get_object_temperature',
            }, {
                'name': 'Emissivity',
                'command': 'get_emissivity', # between 0 - 1  * with object temp  # need diffrenc value for each material!!!
            }]

            setList = {'reset': 'reset'}

            liste = {'get': getList, 'set': setList}

            return liste

    def BrickletJoystick(self, action, uid, cUid=None, value=None):    # Device = Joystick Bricklet
        if action == 'connect':
            try:
                from tinkerforge.bricklet_joystick import Joystick
            except ImportError as err:
                print err
                # if str(uid) == 'hAP':
                #    print 'Joystick Bricklet found...'
            else:
                self.removeUID(uid)
                jsk = Joystick(uid, self.ipcon)     # Create device object JOYSTICK

                jskstr = str(jsk).split()        # get device type
                jskname = jskstr[0].split('.')
                devtype = jskname[2]

                self.deviceList.append({
                    'name': devtype,
                    'instance': jsk,
                    'uid': uid,
                    'cuid': cUid
                })

                # # REGISTER CALLBACKS
                jsk.register_callback(
                    jsk.CALLBACK_PRESSED,  self.cb_pressedjsk)
                jsk.register_callback(
                    jsk.CALLBACK_RELEASED, self.cb_releasedjsk)

                jsk.set_debounce_period(400)                                # Get threshold callbacks with a debounce time of 0.2 seconds (200ms)
                jsk.register_callback(                                      # Register threshold reached callback to function cb_reached
                    jsk.CALLBACK_POSITION_REACHED, self.cb_reachedjsk)
                jsk.set_position_callback_threshold('o', -99, 99, -99, 99)  # Configure threshold for 'x and y value outside of [-99..99]'

                return

        # ~ list - get functions of device!
        if action == 'list':
            getList = [{
                'name': 'Version',
                'command': 'get_api_version',
            }, {
                'name': 'Identity',
                'command': 'get_identity',
            }, {
                'name': 'Position',
                'command': 'get_position',
            }, {
                'name': 'Pressed',
                'command': 'is_pressed',
            }, {
                'name': 'Analog',
                'command': 'get_analog_value',
            }]

            setList = ['reset', 'calibrate']

            liste = {'get': getList, 'set': setList}

            return liste

    def BrickletLCD20x4(self, action, uid, cUid=None, value=None):    # Device = LCD20x4 Bricklet
        getList = [{
            'name': 'Version',
            'command': 'get_api_version'}, {

            'name': 'Identity',
            'command': 'get_identity'}, {

            'name': 'Backlight',
            'command': 'is_backlight_on'}, {

            'name': 'Configuration',
            'command': 'get_config',
        }]

        setList = [{
            'name': 'reset',
            'command': 'reset'}, {

            'name': 'backlight_on',
            'command': 'backlight_on'}, {

            'name': 'backlight_off',
            'command': 'backlight_off'}, {

            'name': 'write_line',
            'command': 'write_line',
            'argument': ['line', 'position', 'text']}
        ]

        if action == 'connect':
            try:
                from tinkerforge.bricklet_lcd_20x4 import LCD20x4
            except ImportError as err:
                print err
                # uid = 'gFt' Display with 4 Buttons
                # uid = '9ew' Display with 3 Buttons
            else:

                self.removeUID(uid)

                #mst = Master(uid, self.ipcon)       # Master Brick
                lcd = LCD20x4(str(uid), self.ipcon)  # LCD20x4

                lcdstr = str(lcd).split()            # get device type
                lcdname = lcdstr[0].split('.')

                devtype = lcdname[2]

                lcd.backlight_on()                  # Turn of LCD Backlight
                lcd.write_line(0, 0, self.unicode_to_ks0066u('name: ' + devtype))
                lcd.write_line(1, 0, self.unicode_to_ks0066u('uid: ' + uid))
                lcd.write_line(2, 0, self.unicode_to_ks0066u('Python Instance: \/ '))
                lcd.write_line(3, 0, self.unicode_to_ks0066u(str(lcd)[58:]))

                self.deviceList.append({
                    'name': devtype,
                    'instance': lcd,
                    'uid': uid,
                    'cuid': cUid
                })
                return

            # # REGISTER CALLBACKS
            #self.lcd.register_callback(self.lcd.CALLBACK_BUTTON_PRESSED,  self.cb_pressedlcd)
            #self.lcd.register_callback(self.lcd.CALLBACK_BUTTON_RELEASED, self.cb_releasedlcd)
            # # END REGISTER CALLBACKS

        # ~ list - get functions of device!
        if action == 'list':

            liste = {'get': getList, 'set': setList}

            return liste

        # ~ list - get functions of device!
        if action == 'set':

            return

    def BrickletRotaryPoti(self, action, uid, cUid=None, value=None):    # Device = Rotary Poti Bricklet
        if action == 'connect':
            try:
                from tinkerforge.bricklet_rotary_poti import RotaryPoti
            except ImportError as err:
                print err
                # if str(uid) == 'g7Q':
                #    print 'Rotary Poti found...'

            else:
                self.removeUID(uid)
                rot = RotaryPoti(uid, self.ipcon)   # Create device object

                rotstr = str(rot).split()        # get device type
                rotname = rotstr[0].split('.')
                devtype = rotname[2]

                self.deviceList.append({
                    'name': devtype,
                    'instance': rot,
                    'uid': uid,
                    'cuid': cUid
                })
                return

        # ~ list - get functions of device!
        if action == 'list':
            getList = [{
                'name': 'Version',
                'command': 'get_api_version',
            }, {
                'name': 'Identity',
                'command': 'get_identity',
            }, {
                'name': 'Position',
                'command': 'get_position',
            }, {
                'name': 'Analog',
                'command': 'get_analog_value',
            }]

            setList = {'reset': 'reset'}

            liste = {'get': getList, 'set': setList}

            return liste

    def BrickletIndustrialQuadRelay(self, action, uid, cUid=None, value=None):    # Device = Industrial Quad Relay
        if action == 'connect':
            try:
                from tinkerforge.bricklet_industrial_quad_relay import IndustrialQuadRelay
            except ImportError as err:
                print err
                # if str(uid) == 'eRN':

            self.iqr = IndustrialQuadRelay(uid, self.ipcon)  # Create device object

    # ###############################################
    # ###############################################
    # ############## # ENUMERATE # ##################
    # ###############################################
    # ###############################################

    def cb_enumerate(self, uid,
                     connected_uid, position,
                     hardware_version, firmware_version,
                     device_identifier, enumeration_type):

        if str(device_identifier) in self.connection_dict:
            self.connection_dict[str(device_identifier)]('connect', str(uid), str(connected_uid))

        if enumeration_type == IPConnection.ENUMERATION_TYPE_DISCONNECTED:
            print("UID:               " + uid)
            print("Enumeration Type:  " + str(enumeration_type))
            self.removeUID(uid)

        self.iwanttoseeyou = False
        if self.iwanttoseeyou:  # Found other Device!
            print("UID:               " + uid)
            print("Enumeration Type:  " + str(enumeration_type))

            if enumeration_type == IPConnection.ENUMERATION_TYPE_DISCONNECTED:
                print("")
                return

            print("Connected UID:     " + connected_uid)
            print("Position:          " + position)
            print("Hardware Version:  " + str(hardware_version))
            print("Firmware Version:  " + str(firmware_version))
            print("Device Identifier: " + str(device_identifier))
            print("")

    def removeUID(self, uid):
        for index, x in enumerate(self.deviceList):
            if x['uid'] == str(uid):  # print 'already exist! - delete the old one!'
                self.deviceList.remove(self.deviceList[index])

    # ###############################################
    # ###############################################
    # ############## # BEAUTIFY # ###################
    # ###############################################
    # ###############################################

    def beautyInt(self, value, divider, unit, threshold):
        resUnit = bc.LtCyan + '\t' + unit + bc.end

        if value >= threshold:
            col = bc.Green + str(value/divider) + bc.end
        else:
            col = bc.Red + str(value/divider) + bc.end

        return col + resUnit

    def beautifyOutput(self, getCommand, getDevice, getName):

        #  DEBUG: Execute Identity cmd: get_identity
        #  DEBUG: Identity(uid='g7Q', connected_uid='6R3jeY', position='a', hardware_version=(1, 1, 0), firmware_version=(2, 0, 2), device_identifier=215)

        if getCommand == 'get_usb_voltage':
            result = getattr(getDevice, getCommand)
            ergebnis = result()

            resHead = bc.LtCyan + '\tUSB Voltage\t: ' + bc.end
            colRes = bc.Green + str(ergebnis/1000.0) + bc.end if ergebnis >= 4800 else bc.Red + str(ergebnis/1000.0) + bc.end
            #resgetCommand = bc.Red + colRes + bc.end
            resUnit = bc.LtCyan + '\tV' + bc.end

            print resHead + colRes + resUnit
            return

        elif getCommand == 'get_illuminance':
            result = getattr(getDevice, getCommand)
            ergebnis = result()

            resHead = bc.LtCyan + '\tIlluminance\t: ' + bc.end

            colRes = self.beautyInt(ergebnis, 10.0, 'Lux', 10)

            print resHead + colRes
            return

        elif getCommand == 'get_humidity':
            result = getattr(getDevice, getCommand)
            ergebnis = result()

            resHead = bc.LtCyan + '\tHumidity\t: ' + bc.end

            colRes = self.beautyInt(ergebnis, 10.0, '%RH', 10)

            print resHead + colRes
            return

        elif getCommand == 'get_analog_value':
            result = getattr(getDevice, getCommand)
            ergebnis = result()

            resHead = bc.LtCyan + '\tAnalog Value\t: ' + bc.end
            colRes = bc.Green + str(ergebnis) + bc.end if ergebnis >= 0 else bc.Red + str(ergebnis) + bc.end

            print resHead + colRes
            return

        elif getCommand == 'get_position':
            result = getattr(getDevice, getCommand)
            ergebnis = result()

            resHead = bc.LtCyan + '\tPosition\t: ' + bc.end
            colRes = bc.Green + str(ergebnis) + bc.end if ergebnis >= 0 else bc.Red + str(ergebnis) + bc.end

            print resHead + colRes
            return

        elif getCommand == 'get_identity':
            result = getattr(getDevice, getCommand)
            ergebnis = result()  # uid='8RG', connected_uid='6R3jeY', position='d', hardware_version=(1, 1, 0), firmware_version=(2, 0, 3), device_identifier=21
            # print ergebnis[0]  # uid
            # print ergebnis[1]  # cuid
            # print ergebnis[2]  # position / port

            # print ergebnis[3]  # hardware version
            hwStack = ''
            for hw in ergebnis[3]:
                hwStack += str(hw) + '.'
            colRes = bc.Green + hwStack[:-1] + bc.end if len(hwStack) >= 4 else bc.Red + hwStack[:-1] + bc.end
            #print bc.LtCyan + '\tHardware Ver.\t: ' + bc.end + colRes

            #print ergebnis[4]  # firmware
            fwStack = ''
            for fw in ergebnis[4]:
                fwStack += str(fw) + '.'
            colRes = bc.Green + fwStack[:-1] + bc.end if len(fwStack) >= 4 else bc.Red + fwStack[:-1] + bc.end
            print bc.LtCyan + '\tFirmware Ver.\t: ' + bc.end + colRes

            #print ergebnis[5]  # device identifier
            colRes = bc.Green + str(ergebnis[5]) + bc.end
            #print bc.LtCyan + '\tDevice ID\t: ' + bc.end + colRes

        elif getCommand == 'get_stack_voltage':
            result = getattr(getDevice, getCommand)
            ergebnis = result()
            print bc.LtCyan + '\tStack Voltage\t: ' + bc.end + bc.Red + str(ergebnis/1000.0) + '\tV' + bc.end

        elif getCommand == 'get_stack_current':
            result = getattr(getDevice, getCommand)
            ergebnis = result()
            print bc.LtCyan + '\tStack Current\t: ' + bc.end + bc.Red + str(ergebnis/1000.0) + '\tA' + bc.end

        elif getCommand == 'get_chip_temperature':
            result = getattr(getDevice, getCommand)
            ergebnis = result()
            if ergebnis >= 1500:
                ergebnis = ergebnis/10.0
            colRes = self.beautyInt(ergebnis, 10.0, '°C', 0)
            print bc.LtCyan + '\tStack Temp\t: ' + bc.end + colRes

        elif getCommand == 'is_pressed':
            result = getattr(getDevice, getCommand)
            ergebnis = result()
            colbool = bc.Green + str(ergebnis) + bc.end if ergebnis else bc.Red + str(ergebnis) + bc.end
            print bc.LtCyan + '\tIs Pressed  \t: ' + bc.end + bc.Red + colbool + bc.end

        elif getCommand == 'is_backlight_on':
            result = getattr(getDevice, getCommand)
            ergebnis = result()
            colbool = bc.Green + str(ergebnis) + bc.end if ergebnis else bc.Red + str(ergebnis) + bc.end
            print bc.LtCyan + '\tBacklight is\t: ' + bc.end + bc.Red + colbool + bc.end

        elif getCommand == 'is_wifi_present':
            result = getattr(getDevice, getCommand)
            ergebnis = result()
            self.haveWifi = ergebnis  # need to saved through multiple calls
            self.colbool = bc.Green + str(ergebnis) + bc.end if ergebnis else bc.Red + str(ergebnis) + bc.end
            #print bc.LtCyan + '\tWifi Available\t: ' + bc.end + bc.Red + self.colbool + bc.end

        elif getCommand == 'get_wifi_status' and self.haveWifi:
            if getCommand == 'get_wifi_status':
                result = getattr(getDevice, getCommand)
                ergebnis = result()
                # print
                # print ergebnis[0]  # mac
                xStack = ''

                print bc.LtCyan + '\tWifi Available\t: ' + bc.end + bc.Red + self.colbool + bc.end

                for arsch in ergebnis[0]:   # convert mac to hex and reverse order!
                    xStack = str(hex(arsch)[2:]) + ':' + xStack
                print bc.LtCyan + '\t     Mac\t: ' + bc.end + bc.Red + xStack[:-1] + bc.end

                # print ergebnis[2]  # channel
                print bc.LtCyan + '\t     Channel\t: ' + bc.end + bc.Red + str(ergebnis[2]) + bc.end

                #print ergebnis[4]  # ip
                yStack = ''
                for loch in ergebnis[4]:
                    yStack = str(loch) + '.' + yStack
                colbool = bc.Green + yStack[:-1] + bc.end if len(yStack) >= 9 else bc.Red + yStack[:-1] + bc.end

                print bc.LtCyan + '\t     IP\t\t: ' + bc.end + bc.Red + colbool + bc.end

                self.haveWifi = False
                self.colbool = ''

        elif getCommand == 'get_api_version':
            result = getattr(getDevice, getCommand)
            ergebnis = result()
            res = str(ergebnis[0])+'.'+str(ergebnis[1])+'.'+str(ergebnis[2])
            #print bc.LtCyan + '\tAPI Version\t: ' + bc.end + bc.Red + res + bc.end

        elif getCommand == 'is_ethernet_present':
            if getCommand == 'is_ethernet_present':
                result = getattr(getDevice, getCommand)
                ergebnis = result()
                self.haveEther = ergebnis  # need to saved through multiple calls
                self.colbool = bc.Green + str(ergebnis) + bc.end if ergebnis else bc.Red + str(ergebnis) + bc.end

        elif getCommand == 'get_ethernet_status' and self.haveEther:
            if getCommand == 'get_ethernet_status':
                result = getattr(getDevice, getCommand)
                ergebnis = result()

                xStack = ''

                print bc.LtCyan + '\tWifi Available\t: ' + bc.end + bc.Red + self.colbool + bc.end

                for arsch in ergebnis[0]:   # convert mac to hex and reverse order!
                    xStack = str(hex(arsch)[2:]) + ':' + xStack
                print bc.LtCyan + '\t     Mac\t: ' + bc.end + bc.Red + xStack[:-1] + bc.end

                # print ergebnis[2]  # channel
                print bc.LtCyan + '\t     Channel\t: ' + bc.end + bc.Red + str(ergebnis[2]) + bc.end

                #print ergebnis[4]  # ip
                yStack = ''
                for loch in ergebnis[4]:
                    yStack += str(loch) + '.'
                print bc.LtCyan + '\t     IP\t\t: ' + bc.end + bc.Red + yStack[:-1] + bc.end

                self.haveWifi = False
                self.colbool = ''

        elif self.debug:
            # print bc.DkWhite + '\tDEBUG: command not found! - cant beautify!!' + bc.end   # JES EI NOW MEI INGLISH IS NOT SE JELLO FROM SE EGG
            result = getattr(getDevice, getCommand)
            print bc.DkWhite + '\tDEBUG: ' + str(result()) + bc.end

    # ###############################################
    # ###############################################
    # ############## # CALLBACKS # ##################
    # ###############################################
    # ###############################################

    # #### CALLBACKS ###########

    def cb_pressedlcd(self, i):   # Callback functions for button status LCD20X4
        # Register pressed buttons - 0 = left, 1 = middle, 2 = right
        if i == 0:
            # Turn backlight on
            #self.lcd.backlight_off() if self.lcd.is_backlight_on() else self.lcd.backlight_on()
            # self.lcd.write_line(0, 0, self.unicode_to_ks0066u('BackLight: ON'))
            pass
        if i == 1:
            pass

        if i == 2:
            pass

        if i == 3:
            pass

    def cb_releasedlcd(self, i):
        # Register released buttons - 0 = left, 1 = middle, 2 = right, 3 = outer right
        if i == 0:
            pass

        if i == 1:
            pass

        if i == 2:
            pass

        if i == 3:
            pass

    # ## MAIN FUNCTION - WITH JOYSTICK I MOVE IN MENU
    def cb_reachedjsk(self, x, y):  # Callback for x and y position outside of [-99..99]

        if y == 100:        # ## UP
            pass

        if y == -100:       # ## DOWN
            pass

        if x == 100:        # ## RIGHT
            pass

        if x == -100:       # ## LEFT
            pass

    def cb_pressedjsk(self):  # Callback function for pressed and released events JOYSTICK
        pass

    def cb_releasedjsk(self):
        pass

    # ################################################################################################
    # ################################################################################################
    # ######## following functions need to be threaded - will block application ######################
    # ################################################################################################
    # ################################################################################################

    # ### START DOOR SPY #####
    def door(self):  # modes are: home, noise or just blank to disable  | showState allow to use LCD
        self.spyDoor = True

        tmpRAM = '1'                                # RAM save last value from door - to verify changes
        while self.spyDoor:
            sleep(2)                                # loop time!
            binTmp = bin(self.io16.get_port('b'))    # get value mask on port b binary
            # print binTmp
            tmpDoor = binTmp[9]                     # catch door bin 0b11111110 latest bit is the door

            if tmpDoor != tmpRAM:                   # if notice changes
                if tmpDoor == '1':                  # OPEN
                    tmpRAM = tmpDoor
                    self.openDoor = True

                    if self.showState:
                        self.lcd.write_line(3, 0, 20*" ")   # 20x Blank to clear last line
                        self.lcd.write_line(3, 0, self.unicode_to_ks0066u('Door: Open!'))

                    if self.mode == 'home':
                        self.toggleLight()

                    if self.mode == 'noise':
                        print 'beep'

                elif tmpDoor == '0':                    # and value[7] == "0":
                    tmpRAM = tmpDoor
                    self.openDoor = False

                    if self.showState:
                        self.lcd.write_line(3, 0, 20*" ")   # 20x Blank to clear last line
                        self.lcd.write_line(3, 0, self.unicode_to_ks0066u('Door: Closed... =)'))

                    if self.mode == 'noise':
                        print 'beep'

    # ### END DOOR SPY #####

    # ### STATE ON LCD SCREEN ####
    def state(self):
        self.showState = True  # code from EVIL ]=}

        while self.showState:
            tmp = str(self.mst.get_chip_temperature()/10)
            tmpAmb = str(self.amb.get_illuminance()/10.0)
            # Write some strings using the unicode_to_ks0066u function to map to the LCD charset
            self.lcd.write_line(0, 0, self.unicode_to_ks0066u('Time: ' + strftime('%H:%M')))
            self.lcd.write_line(1, 0, self.unicode_to_ks0066u('Temperatur:  ' + tmp + '°C'))
            self.lcd.write_line(2, 0, self.unicode_to_ks0066u('Illuminace:  ' + tmpAmb + ' Lux'))
            sleep(1)
    # ### END STATE ####

    # ################################################################################################
    # ################################################################################################
    # ############################## accessable functions for clients  ###############################
    # ################################################################################################
    # ################################################################################################

    def toggleLight(self):
        if self.showLight:
            self.showLight = False

            self.iqr.set_value(0b0000000000000110)  # turn off relay 1
            sleep(1)
            self.iqr.set_value(0b0000000000000000)  # turn off remote
            sleep(1)

        else:
            self.showLight = True

            self.iqr.set_value(0b0000000000001010)    # turn on relay 1
            sleep(1)
            self.iqr.set_value(0b0000000000000000)    # turn off remote
            sleep(1)

    def toggleState(self):  # start & stop state on lcd
        if self.showState:
            self.showState = False
        else:
            t = Thread(target=self.state)
            t.start()

    def toggleDoor(self):  # start & stop state on lcd
        if self.spyDoor:
            self.spyDoor = False
        else:
            t = Thread(target=self.door)
            t.start()

    def beep(self, delay=.5):
        self.io16.set_port_configuration('a', (1 << 0), 'o', True)
        sleep(delay)
        self.io16.set_port_configuration('a', (1 << 0), 'o', False)

    # ### START LCD Status ####
    def status(self, parameter='empty'):
        if parameter == 'empty':

            MasterIDs = []
            for x in self.deviceList:
                if str(x['name']) == 'BrickMaster':  # fetch master bricks
                    MasterIDs.append({               # create list to group them!
                        'uid': x['uid'],
                        'instance': x['instance']
                    })

            if self.debug:
                for x in MasterIDs:
                    print bc.DkWhite + str(x) + bc.end

            for index, master in enumerate(MasterIDs):  # Single Master!

                print
                newDev = bc.Green + 'Master Brick' + bc.end + ': \t' + bc.Red + str(master['uid']) + bc.end
                print newDev
                print len(newDev)*'-'
                # thisStack = '\n' + newDev + '\n' + (len(newDev) * '-') + '\n' + thisStack

                lists = self.BrickMaster('list', str(master['uid']))  # fetch get list

                for cmd in lists['get']:
                    if self.debug:
                        print bc.DkWhite + '\tDEBUG: Execute ' + cmd['name'] + ' cmd: ' + cmd['command'] + bc.end
                        # print bc.DkWhite + '\t' + cmd['command'] + bc.end
                    beautifulOutput = self.beautifyOutput(cmd['command'], master['instance'], cmd['name'])
                    if beautifulOutput:
                        print beautifulOutput

                for x in self.deviceList:
                    if str(x['cuid']) == master['uid']:  # fetch all from this master!

                        print  # Device whitch connected to Master !
                        newBricklet = bc.Green + '\t' + x['name'][8:] + bc.end + ': \t' + bc.Red + str(x['uid']) + bc.end
                        print newBricklet
                        print '\t' + ((len(newBricklet)/2)*'-')

                        if str(x['uid']) == '8RG':  # fetch ambientlight sensor for debugging!
                            lists = self.BrickletAmbientLight('list', str(x['uid']), str(master['uid']))  # fetch get list

                            for cmd in lists['get']:
                                if self.debug:
                                    print bc.DkWhite + '\tDEBUG: Execute ' + cmd['name'] + ' cmd: ' + cmd['command'] + bc.end
                                    # print bc.DkWhite + '\t' + cmd['command'] + bc.end
                                beautifulOutput = self.beautifyOutput(cmd['command'], x['instance'], cmd['name'])
                                if beautifulOutput:
                                    print beautifulOutput
                        else:
                            result = getattr(self, str(x['name']))
                            ergebnis = result('list', str(x['uid']), str(master['uid']))
                            #print ergebnis
                            for cmd in ergebnis['get']:
                                if self.debug:
                                    print bc.DkWhite + '\tDEBUG: Execute ' + cmd['name'] + ' cmd: ' + cmd['command'] + bc.end
                                    # print bc.DkWhite + '\t' + cmd['command'] + bc.end
                                beautifulOutput = self.beautifyOutput(cmd['command'], x['instance'], cmd['name'])
                                if beautifulOutput:
                                    print beautifulOutput

                print len(newDev)*'-'
            return

                                #print x['instance'].get_chip_temperature()

                                #self.connection_dict[str(device_identifier)]('connect', str(uid))

            #state = bc.LtGreen + str(self.showState) + bc.end if self.showState else bc.Red + str(self.showState) + bc.end
            #sDoor = bc.LtGreen + str(self.spyDoor) + bc.end if self.spyDoor else bc.Red + str(self.spyDoor) + bc.end
            #oDoor = bc.LtGreen + str(self.openDoor) + bc.end if self.openDoor else bc.Red + str(self.openDoor) + bc.end
            #light = bc.LtGreen + str(self.showLight) + bc.end if self.showLight else bc.Red + str(self.showLight) + bc.end
            #xmode = bc.LtCyan + self.mode + bc.end

            #print 'showState: \t' + state
            #print 'spyDoor: \t' + sDoor
            #print 'Door is: \t' + oDoor
            #print 'Light is: \t' + light
            #print 'Mode set to: \t' + xmode

        if parameter == "door":   # return boolean | door open?
            binTmp = bin(self.io16.get_port('b'))    # get value mask on port b binary
            # print binTmp
            tmpDoor = binTmp[9]                     # catch door bin 0b11111110 latest bit is the door
            if tmpDoor == '1':                      # OPEN
                return True                         # true = open
            if tmpDoor == '0':
                return False                        # closed

    # ### END LCD Status ####

    # ################################################################################################
    # ################################################################################################
    # ######## Fucking neccessary Functions... #######################################################
    # ################################################################################################
    # ################################################################################################

    # ### START UNICODE TO KOS0006U FOR LCD20x4 ######
    # Maps a Python string to the LCD charset  # IMPORTED NOT FROM MYSELF!!!
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
    # #### STOP UNICODE TO KOS0006U ##################


if __name__ == "__main__":

    try:  # to start TinkerForge Manager
        tinfor = ForgeTinker()
        debug = True
        if debug:
            for x in tinfor.deviceList:                 # access devices from extern!
                if str(x['name']) == 'BrickMaster':     # fetch master brick
                    #print x['instance'].get_chip_temperature()
                    print bc.DkWhite + 'DEBUG: ' + str(x['name']) + ' connected to ' + str(x['cuid']) + bc.end
                else:
                    print bc.DkWhite + 'DEBUG: ' + str(x['name']) + ' connected to ' + str(x['cuid']) + bc.end

        tinfor.run('LimeBlack', tinfor)             # call run to enable the cmdline interface
    except Exception as e:
        print e
        print bc.BgDkRed + bc.Black + 'error in bash...' + bc.end
        print bc.BgDkRed + bc.Black + 'will disconnect now!' + bc.end
        tinfor.quit()
        quit()

    print bc.Red + 'Start Shutting down!' + bc.end
    tinfor.quit()
    quit()
