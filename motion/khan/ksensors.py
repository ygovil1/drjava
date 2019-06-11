from multiplex2 import *
from multiplex import *
import VL53L1X
import time

class ksensors:

	# SW = I2C_SW('I2C switch 0', 0x70, 1)
	# no_chn = 8
	# tof_array = []

	def __init__(self):
		self.sw = I2C_SW('I2C switch 0', 0x70, 1)
		self.no_chn = 8
		self.tof_array = []
		self.thres = 5			# threshold = 5 millimeters

		for i in range(0, self.no_chn):
			self.tof_array.append(VL53L1X.VL53L1X(i2c_bus = 1, i2c_address = 0x29))
			self.tof_array[i].open()			# initialize sensor

	def get_data(self):
		tof_data = []
		for i in range(0, self.no_chn):		# channel = i
    		SW._chn(i) # enable channel at #
    		self.tof_array[i].start_ranging(2) #1,2,3 = ranges
    		distance_in_mm = self.tof_array[i].get_distance()
    		self.tof_data[i].open()
		return tof_data

	def collide(self):
		tof_data = self.get_data(self)
		for i in range(0, self.no_chn):
			if tof_data[i] <= self.thres:
				return True
		return False


if __name__ == '__main__':
	k = ksensors()
	print k.get_data()
	print k.collide()
