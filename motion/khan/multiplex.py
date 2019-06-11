#!/usr/bin/python 

import smbus

class multiplex:
	def __init__(self, bus):
		self.bus = smbus.SMBus(bus)

	def channel(self, address=0x70, channel=0): 
		if (channel == 0): action = 0x04
		elif (channel == 1): action = 0x05
		elif (channel == 2): action = 0x06
		elif (channel == 3): action = 0x07 
		else: action = 0x00 

		self.bus.write_byte_data(address, 0x04, action) 

if __name__ == '__main__':
	bus = 1
	address = 0x70
	plexer = multiplex(bus)
	plexer.channel(address, 3)

	print "Now run i2cdetect"