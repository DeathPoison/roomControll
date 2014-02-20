#!/usr/bin/env python
# consumeservice.py
# consumes a method in a service on the dbus

import dbus
from time import sleep

bus = dbus.SessionBus()
roomcontroll = bus.get_object('org.limeblack.roomcontroll', '/org/limeblack/roomcontroll')
#hello = roomcontroll.get_dbus_method('hello', 'org.limeblack.roomcontroll')
startBoard = roomcontroll.get_dbus_method('startBoard', 'org.limeblack.roomcontroll')
startMenu = roomcontroll.get_dbus_method('startMenu', 'org.limeblack.roomcontroll')
bye   = roomcontroll.get_dbus_method('bye',   'org.limeblack.roomcontroll')
#print hello()
print bye()
sleep(2)
print startBoard()
sleep(2)
print startMenu()
sleep(2)
print bye()
