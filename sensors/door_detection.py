import ksensors
import time
import messageboard
import statistics
import itertools
import signal
import pickle
import csv
from collections import deque

# module = "door", cmd = "location_correction"

#mb = messageboard.MessageBoard("collision")

k = ksensors.ksensors()
history = []
window_size = 6		# must be even num
for i in range(0, k.no_chn):		# init empty deque for each sensor
	history.append(deque([], maxlen = window_size))

# d1 = deque([], maxlen = window_size)			# deque to calculate moving avg
# 												# first half (the wall)
# d2 = deque([], maxlen = window_size)			# second half (where the door is supposed to show up)

# check if valid data (i.e. no noise) by checking if any
# sudden spikes in readings, or if > 1000mm then ignore
# def valid_data(deq):
# 	return 0

nums = []
def handler(*args):
    print('Signal handler called')
    for i in nums:
        print(str(i))
    with open('test_door.pickle', 'wb') as f:
        pickle.dump(nums, f)
    with open('test_door.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(nums)
    exit()
signal.signal(signal.SIGINT, handler)


def noisy_data(l):
	if statistics.stdev(l) > 100:
		return True
	return False


def at_door(deq):
	if len(deq) < 4:
		return (False, None)
	# calculate first half average
	half_len = int(len(deq) / 2)
	first_half = list(itertools.islice(deq, 0, half_len))
	second_half = list(list(itertools.islice(deq, half_len, len(deq))))

	# first, ensure first half isn't noisy, cuz it's supposed to be just wall
	if noisy_data(first_half):
		return (False, None)

	# take averages
	first_avg = sum(first_half) / half_len
	second_avg = sum(second_half) / half_len

	diff = second_avg - first_avg			# second = door > first = wall
	print("Diff:", diff)
	if diff > 60:								# NOTE: this threshold can be changed
		if noisy_data(second_half):
			return (True, True)			# at open door
		else:
			return (True, False)		# at closed door
	else:
		return (False, None)			# not at door


count = 0

while True:
	# no matter what, every iteration, keep track of most recent data points
	# (limit = window_size) for every sensor. Use list of deques
	tof_data = k.update_data()
	str_data = [str(count)]		# to get csv data
	for i in range(0, len(tof_data)):
		history[i].append(tof_data[i])
		str_data.append(str(tof_data[i]))		# to get csv data
	nums.append(str_data)		# to get csv data
	count += 1					# to get csv data

	# now check status because only when near door would we detect door
	target = [ ["state", "updated_state"] ]
#	msg_list = mb.readMsg(target)
#	msg = msg_list[-1]
#	status = msg["status"]
	status = "arrived"

	if status == "arrived":
#		print(history)

	# "arrived" means close to destination, only then would we
	# want to check for door, cuz else then we would see a door
	# that is a different office
		right_back = at_door(history[0])			# (at_door, open)
		right_front = at_door(history[1])
		left_front = at_door(history[6])
		left_back = at_door(history[7])

		door = False
		left = False
		right = False
 		open1 = False

		if right_back[0] and right_front[0]:		# both right sensors at door
			door = True
			right = True
			print(history[0], history[1])
			if right_back[1] and right_front[1]:	# both right sensors open door
				open1 = True
			msg = {
				"at_door": door,
				"left": left,
				"right": right,
				"open": open1
			}
			print(msg)
#			mb.postMsg("updated_state", msg)
		if left_back[0] and left_front[0]:		# both left sensors at door
			door = True
			left = True
			print(history[6], history[7])
			if left_back[1] and left_front[1]:	# both left sensors open door
				open1 = True
			msg = {
				"at_door": door,
				"left": left,
				"right": right,
				"open": open1
			}
			print(msg)
#			mb.postMsg("updated_state", msg)


	time.sleep(0.1)
