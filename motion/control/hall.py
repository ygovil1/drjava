#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#       Hall Effect Sensor
#
# This script tests the sensor on GPIO17.
#
# Author : Matt Hawkins
# Date   : 08/05/2018
#
# https://www.raspberrypi-spy.co.uk/
#
# Import required libraries
import time
import datetime
import RPi.GPIO as GPIO

revA = 0
revB = 0
magA = 0
magB = 0
NUM_MAGNETS = 2 # 2 because 1 full rev would  be 3 magnet counts

def sensorCallback(channel):
  global revA
  global revB
  global magA
  global magB
  global NUM_MAGNETS
# corner case: if sensor starts on low
# Called if sensor output changes
  timestamp = time.time()
  stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
  if GPIO.input(channel):
    # No magnet
    print("Sensor HIGH " + str(channel) + "   " +stamp)
  else:
    # Magnet
    print("Sensor LOW " + str(channel) + "    " +stamp)

    # Update # magnets seen so far
    if channel == 17:
        magA += 1
        print("magA " + str(magA))
    if channel == 27:
        magB += 1

    # Update rev changes
    if magA == NUM_MAGNETS:
        revA += 1
        magA = 0
    if magB == NUM_MAGNETS:
        revB += 1
        magB = 0
    # Compare revs so far
    if revA == revB: #power both motors
        print("power both motors") #driveBoth(20,20)
#        print ("revA  "+ str(revA))
 #       print ("revB "+ str(revB))
    elif revA < revB:
        while revA < revB:
#              print ("revA  "+ str(revA))
#              print ("revB "+ str(revB))
#              print ("power motor A")
               revA += 1
 #              print ("revA   " + str(revA))
    elif revB < revA:
        while revB < revA:
  #              print ("revA  "+ str(revA))
   #             print ("revB "+ str(revB))
#               print  ("power motor B")
                revB += 1
#               print ("revB  " + str(revB))

def main():
  # Wrap main content in a try block so we can
  # catch the user pressing CTRL-C and run the
  # GPIO cleanup function. This will also prevent
  # the user seeing lots of unnecessary error
  # messages.

  # Get initial reading
  sensorCallback(17)
  sensorCallback(27)

  try:
    # Loop until users quits with CTRL-C
    while True :
      time.sleep(0.1)

  except KeyboardInterrupt:
    # Reset GPIO settings
    GPIO.cleanup()

# Tell GPIO library to use GPIO references
GPIO.setmode(GPIO.BCM)

print("Setup GPIO pin as input on GPIO17")

# Set Switch GPIO as input
# Pull high by default
GPIO.setup(17 , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27 , GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(17, GPIO.BOTH, callback=sensorCallback, bouncetime=200)
GPIO.add_event_detect(27, GPIO.BOTH, callback=sensorCallback, bouncetime=200)

if __name__=="__main__":
   main()



