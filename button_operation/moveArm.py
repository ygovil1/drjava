# ----------------- State Codes ----------------
# 0 - not found
# 1 - X centered
# 2 - Y centered
# 3 - move left
# 4 - move right
# 5 - move up
# 6 - move down
# 7 - target lost

import random
import skynet
import messageboard

arm = skynet.robotArm()
arm.ready()
mb = messageboard.MessageBoard('arm')

baseRot = 20

repeatAngleX = 10
repeatAngleY = 10

angleDeltaX = 2
angleDeltaY = 2

previousXDir = -1
previousYDir = -1
previousMoved = None

targetLossThresh = 3
targetsLost = 0

armNeeded = False # is arm needed?

# ------------ arm states ------------
# 0: at rest
# 1: centering, next command
# 2: centering, error
# 3: pressing complete, going back to ready pos

while(True):

    while not armNeeded: # check to see if arm needed
        targetList = mb.readMsg(['nav', 'directions'])
        if len(targetList) == 0:
            continue
        newestTarget = targetList[-1]
        # if shutdown signal, break
        if newestTarget['floor_to'] == 1000:
            arm.rest()
            break
        armNeeded = newestTarget['arm_req']

    # arm is needed, now check for state updates
    trackerStateList = mb.readMsg(['tracker', 'tracker_state'])
    if len(trackerStateList) == 0:
        continue
    newestState = trackerStateList[-1]
    # reset state list to  prevent overlooping
    trackerStateList =  []

    # update state
    state = [newestState['state_1'], newestState['state_2']]
    print('Received state: ', state)

    if state[1] is not None: 
        
        # both centered
        if state[0] == 1 and state[1] == 2:
            print('In reality, I would press the button here')
            mb.postMsg('arm_state', {'state':3})
            continue # dont press for now, get rid of these above lines IRL
            
            # move elbow joint upwards by 10
            # move shoulder joint forwards by 10
            # offsets have to be manually determined
            # Todo: Scale motion by deviation from base angle
            # Right now: effector longer than needed so not a big issue
            currentUpperAngle = arm.getAngle(2) 
            newUpperAngle = currentUpperAngle - 10
            arm.move(2, newUpperAngle)
            arm.move(0, arm.getAngle() - 10)
            mb.postMsg('arm_state', {'state':3})
            armNeeded = False
            arm.ready()

        # x motion first
        elif state[0] != 1:
            if state[0] == 3: # move left
                if previousMoved == 'X' and previousXDir == 4: # we moved too far to the right
                    repeatAngleX -= angleDeltaX
                newAngle = arm.getAngle(1) + repeatAngleX 
                if newAngle > 180: 
                    print('Left motion out of range')
                    continue
                else:                        
                    previousMoved = 'X'
                    previousXDir = 3
                    arm.move(1, newAngle)
            else: # move right
                if previousMoved == 'X' and previousXDir == 3: # we moved too far to the left
                    repeatAngleX -= angleDeltaX
                newAngle = arm.getAngle(1) - repeatAngleX
                if newAngle < 0: 
                    print('Right motion out of range')
                    continue
                else:
                    previousMoved = 'X'
                    previousXDir = 4
                    arm.move(1, newAngle)
        # y motion next
        elif state[1] != 2:
            if state[1] == 5: # move up
                if previousMoved == 'Y' and previousYDir == 6: # we moved too far down
                    repeatAngleY -= angleDeltaY
                newAngle = arm.getAngle(2) - repeatAngleY 
                if newAngle < 0: 
                    print('Upwards motion out of range')
                    continue
                else:
                    previousMoved = 'Y'
                    previousYDir = 5
                    arm.move(2, newAngle)
            else: # move down
                if previousMoved == 'Y' and previousYDir == 5: # we moved too far up
                    repeatAngleY -= angleDeltaY
                newAngle = arm.getAngle(2) + repeatAngleY
                if newAngle > 90: 
                    print('Down motion out of range')
                    continue
                else:
                    previousMoved = 'Y'
                    previousYDir = 6 
                    arm.move(2, newAngle)
    else:    
        if state[0] == -1: # end
            break
        elif state[0] == 0: # searching, move to random position
            # reset
            repeatAngle = 10
            previousXDir = -1
            previousYDir = -1
            
            arm.ready()
            angle = random.randint(90 - baseRot, 90 + baseRot + 1)
            arm.move(1, angle)
        elif state[0] == 7: # correct motion ASSUMPTION: ONLY LOSE TARGET DUE TO MOTION
            
            # deal with target loss due to bad recognition
            targetsLost += 1 
            if targetsLost < targetLossThresh:
                mb.postMsg('arm_state', {'state':1})
                continue
            
            targetsLost = 0
            if previousMoved == 'X': # which motion made us lose it?
                if previousXDir == 3: # we moved left earlier, now move right
                    repeatAngleX -= angleDeltaX # might be error here, < 0
                    newAngle = arm.getAngle(1) - repeatAngleX
                    if newAngle < 0: 
                        print('Right motion out of range')
                        continue
                    else:
                        previousMoved = 'X'
                        previousXDir = 4
                        arm.move(1, newAngle)
                else: # we moved right earlier, now move left
                    repeatAngleX -= angleDeltaX
                    newAngle = arm.getAngle(1) + repeatAngleX 
                    if newAngle > 180: 
                        print('Left motion out of range')
                        continue
                    else:
                        previousMoved = 'X'
                        previousXDir = 3
                        arm.move(1, newAngle)
            else: # correct Y motion
                if previousYDir == 5: # we moved up earlier, now move down
                    repeatAngleY -= angleDeltaY
                    newAngle = arm.getAngle(2) + repeatAngleY
                    if newAngle > 90: 
                        print('Down motion out of range')
                        continue
                    else:
                        previousMoved = 'Y'
                        previousYDir = 6 
                        arm.move(2, newAngle)
                else: # we moved down earier, now move up
                    repeatAngleY -= angleDeltaY
                    newAngle = arm.getAngle(2) - repeatAngleY 
                    if newAngle < 0: 
                        print('Upwards motion out of range')
                        continue
                    else:
                        previousMoved = 'Y'
                        previousYDir = 5
                        arm.move(2, newAngle)
    mb.postMsg('arm_state', {'state':1}) # can use this functionality to handle errors later

sys.exit(0)
