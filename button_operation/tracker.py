# add button recognition module to path
import sys
sys.path.append('./ButtonRec')

import cv2
import bigBrother
from ButtonRec import recognizer

class tracker():

    rec = None
    cam = None
    target = None

    yDims = 480
    xDims = 640
    center = [int(xDims/2), int(yDims/2)]
    effectorYOffset = 110 # effector is this many pixels below center
    pixelRange = 10 
    
    #   ---------------- State Codes ----------------
    # 0 - not found
    # 1 - X centered
    # 2 - Y centered
    # 3 - move left
    # 4 - move right
    # 5 - move up
    # 6 - move down
    # 7 - target lost
    prevState = []

    visualize = None # do i want to see pictures? 
    stateCodes = ['Not found', 'X centered', 'Y centered', 
                  'move left', 'move right', 'move up', 'move down', 'target lost']
    
    def __init__(self, visualize = True):
        self.rec = recognizer.Recognizer()
        self. cam = bigBrother.camera()
        self.visualize = visualize

    def setTarget(self, target):
        # sample validation code
        # not used for now b/c I know what I'm doing
        # if target not in 'BG23':
        #     print('Invalid Target')
        #     return None
        self.target = target
    
    def centerCam(self):
        
        if self.target is None:
            print('No target set')
            return None
        
        frame = self.cam.getFrame()
        seen = False # can we see target?
        currentState = []

        positions, text = self.rec.recognize(frame)

        for pos, char in zip(positions, text):

            if self.visualize:
                p1 = (int(pos[0]), int(pos[1]))
                p2 = (int(pos[2]), int(pos[3]))
                cv2.rectangle(frame, p1, p2, (0, 255, 0), thickness = 2)

                centerX = int((pos[0] + pos[2]) / 2)
                centerY = int((pos[1] + pos[3]) / 2)
                cv2.putText(frame, char, (centerX, centerY), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), thickness = 2)

            if str(self.target) in char:
                
                if seen == True: # duplicate
                    continue
                
                # we can see target
                seen = True
                
                # actual button is second half of detected square
                # (3/4 X, 1/2 Y) of box is center
                buttonCenterX = int(pos[0] + 3 * (pos[2] - pos[0]) / 4)
                buttonCenterY = int(pos[1] + (pos[3] - pos[1]) / 2)

                if self.visualize: cv2.circle(frame, (buttonCenterX, buttonCenterY), 1, [0,0,255], thickness=5)
                    
                # is button within acceptable offset of center screen
                buttonXOffset = abs(buttonCenterX - self.center[0])
                buttonYOffset = abs(buttonCenterY - (self.center[1] + self.effectorYOffset))

                # x centering
                if buttonXOffset <= self.pixelRange:
                    currentState.append(1)
                elif buttonCenterX > self.center[0] + self.pixelRange: # button is too much to the right
                    currentState.append(4)
                else: # button is too much to the left
                    currentState.append(3)

                # y centering
                if buttonYOffset <= self.pixelRange:
                    currentState.append(2)
                elif buttonCenterY > self.center[1] + self.effectorYOffset + self.pixelRange: # button is too far down
                    currentState.append(6)
                else: # button is too far up
                    currentState.append(5)

        if not seen and len(self.prevState) != 0 and 0 not in self.prevState: # we saw it and lost it 
            currentState.append(7)
        elif not seen: # we haven't seen it before
            currentState.append(0) 
                
        if self.visualize: 
            outString = '' 
            for s in currentState:
                outString += self.stateCodes[s] + ' '
            cv2.putText(frame, outString, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness = 2)
            
            cv2.circle(frame, (self.center[0], self.center[1]), 1, [0,0,255], thickness=5)
            cv2.circle(frame, (self.center[0], self.center[1] + self.effectorYOffset), 1, [255,255,0], thickness=5)

        self.prevState = currentState
        if self.visualize: return currentState, frame
        else: return currentState