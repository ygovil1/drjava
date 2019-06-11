#    Program: basic.py
# Descrption: tests serial port communication, 
#             basic forward/reverse commands to sabertooth. 
#

from pysabertoothLocal import Sabertooth
import time




class drJava:
    """
    Instantiates drJava object
    """
    test = Sabertooth("/dev/tty.Bluetooth-Incoming-Port", baudrate=9600, address=128, timeout=0.1)
    # def __init__(self):
    #     print("This is the constructor method.")
    #     saber = Sabertooth("/dev/tty.Bluetooth-Incoming-Port", baudrate=9600, address=128, timeout=0.1)
    #     print (saber.info())
    #     self.saber = saber




    # def forward(self, speed):
    #     self.driveBoth(speed, speed)

    # def reverse(self, speed):
    #     self.driveBoth(speed, speed)

    # def turnRight(self, speed):
    #     "Turn right"

    # def turnLeft(self, speed):
    #     "Turn left"

    # def getInPosition(self, speed):
    #     "Get ready to get into elevator"

    # def getInElevator():
    #     "Get into elevator"




    # mixed mode for turning 

def main():
    """Testing"""
    example = drJava()
    example.test
    

    
    print ("Hello")




if __name__ == "__main__":
        main()