#!/usr/bin/env python
# -*- coding: utf-8 -*-  

HOST = "localhost"
PORT = 4223
UID = "5VkWAv" # Change to your UID

from time import sleep

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_servo import Servo

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    servo = Servo(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Configure two servos with voltage 5.5V
    # Servo 1: Connected to port 0, period of 19.5ms, pulse width of 1 to 2ms
    #          and operating angle -100 to 100°
    #
    # Servo 2: Connected to port 5, period of 20ms, pulse width of 0.95 
    #          to 1.95ms and operating angle -90 to 90°
    servo.set_output_voltage(5500)

    servo.set_degree(0, -9000, 9000)
    servo.set_pulse_width(0, 800, 2400)
    servo.set_period(0, 19500)
    servo.set_acceleration(0, 65000) # Slow acceleration
    servo.set_velocity(0, 65000) # Full speed ~ 0x#### 

#    servo.set_degree(5, -9000, 9000)
#    servo.set_pulse_width(5, 1000, 2000)
 #   servo.set_period(5, 19500)
  #  servo.set_acceleration(5, 55000) # Full acceleration
   # servo.set_velocity(5, 65000) # Full speed
#
    servo.set_position(0, 9000) # Set to most right position
    servo.enable(0)

    #servo.set_position(5, -9000) # Set to most left position
    #servo.enable(5)

    sleep(2)

    servo.set_position(0, -9000) # Set to most right position
    servo.enable(0)
    sleep(4)
    servo.set_position(0, 9000) # Set to most right position
    servo.enable(0)
    sleep(0.5)
    servo.set_position(0, -9000) # Set to most right position
    servo.enable(0)
    sleep(2)
    servo.set_position(0, 9000) # Set to most right position
    servo.enable(0)
    sleep(2)
    servo.set_position(0, -9000) # Set to most right position
    servo.enable(0)
    sleep(2)
    servo.set_position(0, 9000) # Set to most right position
    servo.enable(0)

    #servo.set_position(5, 9000) # Set to most left position
    #servo.enable(5)


    raw_input('Press key to exit\n') # Use input() in Python 3
    ipcon.disconnect()