import grovepi
import time

waterpomp = 8

WATERON_MODE = 1
WATEROFF_MODE = 0

class Pomp:
	def __init__(self):
		self.mode = WATEROFF_MODE
		self.waterlimit = 10

	def switch(self):
		grovepi.pinMode(waterpomp,"OUTPUT")
		grovepi.digitalWrite(waterpomp,self.mode)
		grovepi.pinMode(waterpomp, "INPUT")
		print("mode:"+str(self.mode))