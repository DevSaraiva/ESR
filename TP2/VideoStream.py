class VideoStream:
	def __init__(self, filename, database):
		self.filename = filename
		self.database = database
		self.frameNum = 0
		

	def run(self):
		pass
	
	def nextFrame(self):
		"""Get next frame."""
		data = self.file.read(5) # Get the framelength from the first 5 bits
		if data: 
			framelength = int(data)

			# Read the current frame
			data = self.file.read(framelength)
			self.frameNum += 1
		return data
		
	def frameNbr(self):
		"""Get frame number."""
		return self.frameNum
	
