#!/usr/bin/env python
# -*- coding: utf-8 -*-  

HOST = "localhost"
PORT = 4223
stUID = "6jDX7j" # Change to your UID
poUID = "8Cu"

from time import sleep

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_stepper import Stepper
from tinkerforge.bricklet_rotary_poti import RotaryPoti

def cb_position(position):
    velo = 0xFFFF / 2 * position / 150
    print velo
    stepper.set_steps(velo) # Drive 60000 steps forward
    #sleep(2)

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    stepper = Stepper(stUID, ipcon) # Create device object
    poti = RotaryPoti(poUID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected
   
    # Set Period for position callback to 0.05s (50ms)
    # Note: The position callback is only called every 50ms if the 
    #       position has changed since the last call!
    poti.set_position_callback_period(50)

    # Register position callback to function cb_position
    poti.register_callback(poti.CALLBACK_POSITION, cb_position)
   
    stepper.set_motor_current(800) # 800mA
    stepper.set_step_mode(1) # 1/8 step mode
    stepper.set_max_velocity(1000) # Velocity 2000 steps/s

    # Slow acceleration (500 steps/s^2), 
    # Fast deacceleration (5000 steps/s^2)
    stepper.set_speed_ramping(2000, 5000) 

    stepper.enable()
    stepper.set_steps(6000) # Drive 60000 steps forward

    raw_input('Press key to exit\n') # Use input() in Python 3
    ipcon.disconnect()