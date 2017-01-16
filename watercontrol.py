import paho.mqtt.client as mqtt
import watering
import time
import threading

WATERON_MODE = 1
WATEROFF_MODE = 0
STANDBY_OK = 1
STANDBY_NG = 0
waterlimit = 10

host ="localhost"
port = 1883
topic = "#"

def over():
    watering.standby = STANDBY_OK
    print("standby:"+str(watering.standby))
    if watering.mode == WATERON_MODE:
	watering.mode = WATEROFF_MODE
	watering.switch()
	print("watering is over")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.payload))
    action = msg.payload
    t=threading.Timer(waterlimit, over)
    if action == "wateron":
	if watering.standby == STANDBY_OK:
	    watering.mode = WATERON_MODE
	    watering.switch()
	    print("received watering order")
	    watering.standby = STANDBY_NG
	    print("standby:" + str(watering.standby))
	    t.start()
	else:
	    print("wait a second")
    if action == "wateroff" and watering.mode == WATERON_MODE:
	watering.mode = WATEROFF_MODE
	watering.switch()
	print("received stop_watering order")

watering = watering.Pomp()
watering.mode = WATEROFF_MODE

if __name__ == '__main__':
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port=port, keepalive=60)

    client.loop_forever()