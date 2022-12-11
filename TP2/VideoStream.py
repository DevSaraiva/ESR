
from time import sleep

class VideoStream:
	def __init__(self, filename, database):
		self.filename = filename
		self.database = database
		self.frameNum = 0

	def run(self):
		pass
	
	def nextFrame(self):
	
		nextframe = self.database.popStreamPacket(self.filename)
		self.frameNum += 1

		print(nextframe)
		
		return nextframe

		
	def frameNbr(self):
		"""Get frame number."""
		return self.frameNum
	
