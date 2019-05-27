import sys
import cv2
import time
import tracker
import messageboard

# create messageboard for button tracker
# can get messages since creation of MB
# or since last read
mb = messageboard.MessageBoard('tracker')

waitForArm = False
targetReceived = False
target = None
state1 = None
state2 = None
state = None
vis = True

# create tracker
tracker = tracker.tracker(visualize=vis)

while(True):

    if not targetReceived:
        # check messageboard once every second
        # time.sleep(1) 
        
        # check messageboard for target
        targetList = mb.readMsg(['nav', 'directions'])

        # if no new commands
        if len(targetList) == 0: continue
        else:
            newestTarget = targetList[-1]
            # if shutdown signal, break
            if newestTarget['floor_to'] == 1000:
                print('Exit code received, program terminated')
                break
            # if arm not needed continue
            elif not newestTarget['arm_req']:
                continue
            else:
                targetReceived = True # proceed to rest of loop
                target = newestTarget['floor_to']
                print('Received new target, floor ', end = '')
                print(target)
                tracker.setTarget(target)
    elif not waitForArm:
        # center camera, get state
        if vis:
            state, frame = tracker.centerCam()
            cv2.imshow('Video Stream', frame)
        else:
            state = tracker.centerCam()

        print(state)

        if len(state) == 2:
            state1 = state[0]
            state2 = state[1]
        else:
            state1 = state[0]
            state2 = None
        
        # post to messageboard
        mb.postMsg('tracker_state', {'state_1': state1, 'state_2': state2})
        waitForArm = True
        # ------------ arm states ------------
        # 0: at rest
        # 1: centering, next command
        # 2: centering, error
        # 3: pressing complete, going back to ready
    elif waitForArm:
        # wait for arm response
        armStateList = mb.readMsg(['arm', 'arm_state'])
        print('Waiting for arm state...')
        if len(armStateList) == 0:
            continue
        newestState = armStateList[-1]
        armState = newestState['state']
        print('Received arm state ', end = '')
        print(armState)
        if armState == 0: # something wrong, we told it to move 
            continue # handle error here
        elif armState == 1: #centering, next command
            waitForArm = False
        elif armState == 2: # something wrong, probably out of range
            continue # handle error here
        elif armState == 3: # finshed pressing, reset values
            targetReceived = False
            target = None
            state1 = None
            state2 = None
            state = None

cv2.destroyAllWindows()
sys.exit(0)