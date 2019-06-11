from multiplex2 import * 
from multiplex import *
import VL53L1X 
import time
import signal 
import pickle
import csv

nums = []

def handler(signum, frame):
    print ('Signal handler called with signal', signum)
    for i in nums:
        print str(i)
    with open('test.pickle', 'wb') as f:
        pickle.dump(nums, f)
    with open('test.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(nums)
        
    exit()

signal.signal(signal.SIGINT, handler)
    
SW = I2C_SW('I2C switch 0', 0x70, 1) 

no_chn = 8
tof_array = []
for i in range(0, no_chn):
	tof_array.append(VL53L1X.VL53L1X(i2c_bus = 1, i2c_address = 0x29))
	tof_array[i].open()

print("Time \t \t Right:0 \t Midright:1 \t Midleft:2 \t Left:3") 

count = 0
while(True): 		# outer loop for timer, runs every 10 sec	
	# loop through all channels to print sensor readings
	# one at a time (1 sensor / channel)
	t = str(time.strftime("%m/%d %H:%M:%S")) # US Time
	readings = t + "\t"
	
#	subSW._chn(0)
#	subTOF = VL53L1X.VL53L1X(i2c_bus = 1, i2c_address = 0x29)
#	subTOF.open()
#	subTOF.start_ranging(2)
#	d = subTOF.get_distance()
#	print("sub tof: ", d)

        thisRead = [str(count)]
        for i in range(0, no_chn):		# channel = i
		SW._chn(i) # enable channel at # 
		# tof = VL53L1X.VL53L1X(i2c_bus = 1, i2c_address = 0x29)
		# tof_array[i].open()
		tof_array[i].start_ranging(2) #1,2,3 = ranges
		distance_in_mm = tof_array[i].get_distance()
		readings = readings + str(i) + ":" + str(distance_in_mm) + "\t\t"
                thisRead.append(str(distance_in_mm))

        nums.append(thisRead)
        count += 1
        
	print(readings)

	time.sleep(0.10)
