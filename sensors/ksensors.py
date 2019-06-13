from multiplex2 import *
from multiplex import *
import math
import VL53L1X
import time

class ksensors:

	# SW = I2C_SW('I2C switch 0', 0x70, 1)
	# no_chn = 8
	# tof_array = []

	def __init__(self):
		# bus = 1
		# address = 0x70
		# plexer = multiplex(bus)
		# plexer.channel(address, 3)

		self.sw = I2C_SW('I2C switch 0', 0x70, 1)
		self.no_chn = 8
		self.tof_array = []
		self.thres = 200			# threshold = 5 millimeters

		for i in range(0, self.no_chn):
			self.tof_array.append(VL53L1X.VL53L1X(i2c_bus = 1, i2c_address = 0x29))
			self.tof_array[i].open()			# initialize sensor



	def update_data(self):
		tof_data = []
		for i in range(0, self.no_chn):		# channel = i
    			self.sw._chn(i) # enable channel at #
    			self.tof_array[i].start_ranging(2) #1,2,3 = ranges
    			distance_in_mm = self.tof_array[i].get_distance()
    			tof_data.append(distance_in_mm)
		return tof_data



	def get_data(self):					# return a tuple of (left/right, theta) in (0/1, radians)
		# note: hallway width = 170cm, so if sensors on 1 side < half of 170,
		# then closer to that wall
		length = 277				# dist btwn 2 sensors = 27.7cm; length of robot = 61cm; width = 51cm
		facing_wall = None						# 0 = left, 1 = right
		theta = None

		tof_data = self.update_data()
		right_back 	= tof_data[0]
		right_front = tof_data[1]
		left_front 	= tof_data[6]
		left_back 	= tof_data[7]
		if left_back < 850 and left_front < 850: # closer to right --> doing this cuz assuming closer the range, the more accurate the data
			print("left")
			print(left_back, left_front)
			tan_theta = math.fabs(left_back - left_front) / length
			theta = math.atan(tan_theta)

			print("right")
			print (right_back, right_front)
			tan_theta = math.fabs(right_back - right_front) / length
			print ("right", math.atan(tan_theta))

			if left_front < left_back: 		# facing towards right wall
				facing_wall = 0
			else:
				facing_wall = 1
		else:							# closer to left
			print ("right")
			print (right_back, right_front)
			tan_theta = math.fabs(right_back - right_front) / length
			theta = math.atan(tan_theta)
			if (right_front < right_back): 		# facing towards right wall
				facing_wall = 1
			else:
				facing_wall = 0
		return theta # (facing_wall, theta)



	def collide(self):
		tof_data = self.update_data()
		front_thres = self.thres
		side_thres = self.thres - 150
		for i in range(2, 6):			# just front camera
			if tof_data[i] <= front_thres and tof_data[i] > 0:
				print (i, tof_data[i])
				return True
		if tof_data[0] <= side_thres and tof_data[0] > 0:
			print (0, tof_data[0])
			return True
		if tof_data[1] <= side_thres and tof_data[1] > 0: 	# right side too close to wall
			print (1, tof_data[1])
			return True
		if tof_data[6] <= side_thres and tof_data[6] > 0:
			print (6, tof_data[6])
			return True
		if tof_data[7] <= side_thres and tof_data[7] > 0:	# left side
			print (7, tof_data[7])
			return True
		return False




if __name__ == '__main__':
	k = ksensors()
	print(k.get_data())
	print(k.collide())
