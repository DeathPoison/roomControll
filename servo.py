#!/usr/bin/env python
# -*- coding: utf-8 -*-  

HOST = "localhost"
PORT = 4223
seUID = "5VkWAv" # Change to your UID
poUID = "8Cu"

from time import sleep

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_servo import Servo
from tinkerforge.bricklet_rotary_poti import RotaryPoti

def cb_position(position):
    velo = 0xFFFF / 2 * position / 150
    print velo
    servo.set_position(0, velo) # Set to most right position
    servo.set_position(5, velo) # Set to most right position

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    servo = Servo(seUID, ipcon) # Create device object
    poti = RotaryPoti(poUID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected
   
    # Set Period for position callback to 0.05s (50ms)
    # Note: The position callback is only called every 50ms if the 
    #       position has changed since the last call!
    poti.set_position_callback_period(50)

    # Register position callback to function cb_position
    poti.register_callback(poti.CALLBACK_POSITION, cb_position)



    # Configure two servos with voltage 5.5V
    # Servo 1: Connected to port 0, period of 19.5ms, pulse width of 1 to 2ms
    #          and operating angle -100 to 100°
    #
    # Servo 2: Connected to port 5, period of 20ms, pulse width of 0.95 
    #          to 1.95ms and operating angle -90 to 90°
    servo.set_output_voltage(5500)

    servo.set_degree(0, -32767, 32767)
    servo.set_pulse_width(0, 800, 2400)
    servo.set_period(0, 19500)
    servo.set_acceleration(0, 0xFFFF) # Slow acceleration
    servo.set_velocity(0, 0xFFFF) # Full speed ~ 0x#### 

    servo.set_degree(5, -32767, 32767)
    servo.set_pulse_width(5, 1200, 1800)
    servo.set_period(5, 19500)
    servo.set_acceleration(5, 0xFFFF) # Full acceleration
    servo.set_velocity(5, 0xFFFF) # Full speed
#
    servo.enable(0)
    servo.enable(5)

##    servo.set_position(0, -9000) # Set to most right position
##    servo.enable(0)
##    sleep(4)
##    servo.set_position(0, 9000) # Set to most right position
##    servo.enable(0)
##    sleep(0.5)

    raw_input('Press key to exit\n') # Use input() in Python 3
    ipcon.disconnect()