import grovepi
import time

portnumber = 8

WATERON_MODE = 1
WATEROFF_MODE = 0

class Pomp:
	def __init__(self):
		self.mode = WATEROFF_MODE
		self.waterlimit = 10

	def switch(self):
		grovepi.pinMode(portnumber,"OUTPUT")
		grovepi.digitalWrite(portnumber,self.mode)
		print("mode:"+str(self.mode))