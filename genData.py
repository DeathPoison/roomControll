#!/usr/bin/env python
# -*- coding: utf-8 -*-  

HOST = "localhost"
PORT = 4223
alUID = "8RG" # Change to your UID
iqrUID = "eRN" # Change to your UID

import time

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ambient_light import AmbientLight

# Callback for illuminance without threshold
def cb_illuminance(ilu):
    fo.write( "\t'lux '\t:\t'" + str(ilu) + "',\n" );
    fo.write( "\t'date'\t:\t'" + time.strftime("%d.%m.%Y um %H:%M:%S Uhr") + "',\n" );
    time.sleep(1)

def cb_graph(ilu):
    play.write( str( ilu/10 ) + "\t" )

    tmpIlu = ilu/10
    tmpBar = ":-"
    while tmpIlu >= 0:
        tmpBar = tmpBar + ":-"
        tmpIlu = tmpIlu - 20

    play.write( tmpBar + '\n' );



if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    al = AmbientLight(alUID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd

    # Open File to save data in there
    fo = open('ambData.json', 'wb')
    play = open('niceGraph.txt', 'wb')

    al.set_illuminance_callback_period(10)
    al.register_callback(al.CALLBACK_ILLUMINANCE, cb_illuminance)

    al.set_illuminance_callback_period(10)
    al.register_callback(al.CALLBACK_ILLUMINANCE, cb_graph)

    fo.write( '{\n' );

    raw_input('Press key to exit\n') # Use input() in Python 3

    fo.write( '\n}' );
    fo.close

    play.close

    ipcon.disconnect()
