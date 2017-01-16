import grovepi
import time

pinnumber = 8

WATERON_MODE = 1
WATEROFF_MODE = 0

class Pomp:
	def __init__(self):
		self.mode = WATEROFF_MODE

	def switch(self):
		grovepi.pinMode(pinnumber,"OUTPUT")
		grovepi.digitalWrite(pinnumber,self.mode)
		print("mode:"+str(self.mode))