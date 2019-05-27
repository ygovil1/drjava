from adafruit_servokit import ServoKit

NUM_CHANNELS = 16 # number of channels on controller
#UPPER_ARM_LENGTH = 16.0  # cm, to end effector
#LOWER_ARM_LENGTH = 13.0 # cm	
#UPPER_ARM_ANGLE = math.radians(0) # between upper arm and upper horizontal
#LOWER_ARM_ANGLE = math.radians(40 - 12) # between lower arm and lower horizontal

#-----servo mappings------
# 0 - lower arm angle
# 1 - base rotation
# 2 - upper arm angle
# 3 - head swivel
# 4 - head rotation
# 5 - upper arm rotation

class robotArm():
		
    controller = None
    servos = None
	
    def __init__(self):
        self.controller = ServoKit(channels = NUM_CHANNELS)
        self.servos = self.controller.servo

	# sets arm to rest position	
    def rest(self):	
        self.servos[0].angle = 180
        self.servos[1].angle = 90
        self.servos[2].angle = 0
        self.servos[3].angle = 90
        self.servos[4].angle = 90
        print('Arm set to rest position')
		
    # sets arm to ready position	
    def ready(self):
        self.servos[0].angle = 95
        self.servos[1].angle = 90
        self.servos[2].angle = 40 # 12 = 90 in cartesian
        self.servos[3].angle = 90
        self.servos[4].angle = 0
        self.servos[5].angle = 180
        print('Arm set to ready position')

    # return current angle of specified servo
    def getAngle(self, servo):
        return self.servos[servo].angle

    # move servo to specified angle
    def move(self, servo, angle):
        self.servos[servo].angle = angle
