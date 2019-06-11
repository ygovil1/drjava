#     Program: elavator.py
# Description: Implements elevator motion i.e. get in position 
#              and enter elevator, get in position and exit. 
#

from pysabertooth import Sabertooth
import time

saber = Sabertooth("/dev/", baudrate=9600, address=128, timeout=0.1)

def getInPosition():
    "Gets robot in position"

def enterElevator():
    "Enters elevator"

def getOutPosition():
    "Robot gets in position to exit elevator"
def exitElevator():
    "Exits elevator"