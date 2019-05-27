import sys
import messageboard
mb = messageboard.MessageBoard('nav')

while(True):
    print('Enter target button, 1000 to exit')
    button = int(input())
    armStateList = mb.readMsg(['arm', 'arm_state'])
    print(len(armStateList))
    if button == 1000: 
        mb.postMsg('directions', {'arm_req':False, 'floor_to':button})
        break
    else: mb.postMsg('directions', {'arm_req':True, 'floor_to':button})

sys.exit()
    
