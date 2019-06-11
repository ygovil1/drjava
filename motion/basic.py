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

saber.drive(1, 10)   # forward 
saber.drive(2, 10)
saber.stop()
time.sleep(15)

saber.drive(1, -10)  # reverse 
saber.drive(2, -10)
time.sleep(5)


saber.driveBoth(0, 5) # slight right turn
saber.driveBoth(5, 0) # slight left turn
saber.stop()
saber.close()    