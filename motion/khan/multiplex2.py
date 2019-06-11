# !/usr/bin/python
# I2C address: 70 - 77 
# Channel: 0 - 7 

import smbus 

# class for i2c switch 
class I2C_SW(object):
	def __init__(self, name, address, bus_nr): 
		self.name = name
		self.address = address 
		self.bus_nr = bus_nr 
		self.bus = smbus.SMBus(bus_nr)

	# change to i2c channel 0...7
	def _chn(self, channel):
		self.bus.write_byte(self.address, 2**channel)

	# block all channels read only the main i2c (onw hich is the addr SW)
	def _rst(self):
		self.bus.write_byte(self.address, 0)
		print self.name, ' ', 'Switch reset' 

	# read all 8 channels
	def _all(self): 
		self.bus.write_byte(self.address, 0xff)
		print self.name, ' ', 'Switch read all lines' 

if __name__ == '__main__':
	bus = 1
	address = 0x70
	SW = I2C_SW('I2C switch 0', address, bus)
	SW._all()
	SW._rst()
	# to enable channel: SW._chn(channel number 0-7)
	# check with i2cdetect y -1 (if bus_nr = 1)

	print "Done"