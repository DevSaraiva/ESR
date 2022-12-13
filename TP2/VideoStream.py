
from time import sleep

class VideoStream:
	def __init__(self, filename, database):
		self.filename = filename
		self.database = database
		self.frameNum = 0
		self.receiverId = -1
		tryVar = False
		while tryVar == False:
			self.receiverId = database.addStreamReceiver(filename)
			tryVar = self.receiverId
			

	def run(self):
		pass
	
	def nextFrame(self):
	
		print('videoStream ',self.receiverId)
		nextframe = self.database.popStreamPacket(self.filename,self.receiverId)
		self.frameNum += 1
		
		return nextframe

		
	def frameNbr(self):
		"""Get frame number."""
		return self.frameNum
	
