#    Program: basic.py
# Descrption: tests serial port communication, 
#             basic forward/reverse commands to sabertooth. 
#

from pysabertooth import Sabertooth
import time

saber = Sabertooth("/dev/serial0", baudrate=9600, address=128, timeout=0.1)

def forward(speed):
     saber.driveBoth(speed, speed)

def reverse(speed):
     saber.driveBoth(speed, speed)


# mixed mode for turning 
