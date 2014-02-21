#!/usr/bin/env python
# consumeservice.py
# consumes a method in a service on the dbus

import dbus
from time import sleep

import argparse  # argument is key and option is --key...

def status(DBObject):
    runStatus = DBObject.get_dbus_method('status', 'org.limeblack.roomcontroll')
    print runStatus()

def bye(DBObject):
    runBye = DBObject.get_dbus_method('bye', 'org.limeblack.roomcontroll')
    print runBye()

def startBoard(DBObject):
	runStartBoard = DBObject.get_dbus_method('startBoard', 'org.limeblack.roomcontroll')
	print runStartBoard()

def startMenu(DBObject):
    runStartMenu = DBObject.get_dbus_method('startMenu', 'org.limeblack.roomcontroll')
    print runStartMenu()


if __name__ == "__main__":
    try:

        bus = dbus.SessionBus()
        roomcontroll = bus.get_object('org.limeblack.roomcontroll', '/org/limeblack/roomcontroll')
        #hello = roomcontroll.get_dbus_method('hello', 'org.limeblack.roomcontroll')
        #status     = roomcontroll.get_dbus_method('status', 'org.limeblack.roomcontroll')
        #startBoard = roomcontroll.get_dbus_method('startBoard', 'org.limeblack.roomcontroll')
        #startMenu  = roomcontroll.get_dbus_method('startMenu',  'org.limeblack.roomcontroll')
        #bye        = roomcontroll.get_dbus_method('bye',        'org.limeblack.roomcontroll')

        parser = argparse.ArgumentParser()
        parser.add_argument('action', help="actions are: status, startBoard, startMenu, bye")
        args = parser.parse_args()

        function_dict = {'status':status, 'bye':bye, 'startMenu':startMenu, 'startBoard':startBoard }

        function_dict[args.action](roomcontroll)
        
    except Exception as errtxt:
        print errtxt
