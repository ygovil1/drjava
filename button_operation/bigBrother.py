import cv2
from threading import Thread

class camera():

	stream = None # video stream
	frame = None # current frame
	terminate = False # terminate video stream?

	def __init__(self):
		self.stream = cv2.VideoCapture(0)

		# reduces delay to 3 frames without threading
		self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1) 
		
		# initial read of frame
		_, self.frame = self.stream.read()
		
		# start thread
		Thread(target = self.emptyBuffer, args = ()).start()

		print('Video stream initialized')
	
	# grab frames from camera on new thread
	def emptyBuffer(self):
		while not self.terminate:
			_, self.frame = self.stream.read()

	# get current frame
	def getFrame(self):
		return self.frame
	
	# visualize video stream 	
	def visualizeStream(self):
		while(True):
			frame = self.frame
			cv2.imshow('Video Stream', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		cv2.destroyAllWindows()
		
	# close video stream	
	def close(self):
		self.terminate = True
		self.stream.release()
		print('Video stream closed')