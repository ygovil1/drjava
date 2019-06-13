import ksensors
import time
import messageboard

print "hello"
k = ksensors.ksensors()
state = False 		# False = STOP!; True = GO
print "hello"
mb = messageboard.MessageBoard("collision")
# print(str(mb))


# module = "collision", cmd = "collision_prevention"
while True:
	if not state: 				# currently stopped
		if not k.collide(): 	# but no obstalces
			state = True
			mb.postMsg("collision_prevention", {"collide": False}) # no collision, GO!
			target = [ ["collision", "collision_prevention"] ]
			print state
			msg_list = mb.readMsg(target)
			msg = msg_list[-1]
			print msg
	else: 						# currently going
		if k.collide():  		# but about to collide --> STOP!
			# send message to message board
			state = False
			mb.postMsg("collision_prevention", {"collide": True}) # collision, STOP!
			target = [ ["collision", "collision_prevention"] ]
			print state
			msg_list = mb.readMsg(target)
			msg = msg_list[-1]
			print msg


	time.sleep(0.1)
