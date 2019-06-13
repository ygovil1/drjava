import ksensors
import time
import messageboard

k = ksensors.ksensors()
state = False 		# False = STOP!; True = GO
mb = messageboard.MessageBoard("collision")
# print(str(mb))


def goodPosition(x, y):
	# 	area1 =
	# 		bottom left : 108, 85px
	# 		top right : 132, 67px
	# 	area2 =
	# 		bottom left: 180, 85px
	# 		top right: 206, 68px
	# 	area3 =
	# 		bottom left: 251, 85px
	# 		top right: 281, 67px
	if y >= 67 and y <= 85:
		if x >= 108 and x <= 132: 	# area1
			return True
		else if x >= 180 and x <= 206: # area2
			return True
		else if x >= 251 and x <= 281:
			return True
	return False


while True:
	target = ["state", "updated_state"]			# read from State
	# begin_ts = 1200
	msg_list = mb.readMsg(target)					# is ts necessary?
	if len(msg_list) <= 0:
		continue
	msg = msg_list[-1]
	# first, check if in "good" place to calculate angle
	x = msg['x_pos_pixels']
	y = msg['y_pos_pixels']
	if goodPosition(x,y):
		angle = k.get_data()
		mb.postMsg("angle_correction", {"angle": theta})

	time.sleep(0.1)

	# “x_pos_meters”: float,
	# “y_pos_meters”: float,
	# “x_pos_pixels”: float,
	# “y_pos_pixels”: float,
	# “orientation”: x / -x,
	# “angle”: float (radians),
	# “status”: delivering / idle / dead
