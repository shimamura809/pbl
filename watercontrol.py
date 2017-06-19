import paho.mqtt.client as mqtt
import watering
import time
import threading
import datetime
import os
from pub import temperature, illuminance, moisture

WATERON_MODE = 1
WATEROFF_MODE = 0
START_SEC  =    datetime.datetime.today()

water_limit = 10  #1<water_limit<60

host ="210.152.14.37"
# host = "localhost"
port = 1883
topic = "#"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    action = msg.payload
    if action == "wateron":
    	global START_SEC
    	START_SEC  =    datetime.datetime.today()
#    	print(START_SEC)
    	watering.mode = WATERON_MODE
    	watering.switch()
    elif action == "wateroff":
    	watering.mode = WATEROFF_MODE
    	watering.switch()
    elif msg.topic == "get":
        d = datetime.datetime.today()
        dstr = d.strftime('%Y-%m-%d %H:%M:%S')
        client.publish("AIoT/data/", "datetime:"+dstr+"/temperature:"+str(temperature())+"/moisture:"+str(moisture())+"/illuminance:"+str(illuminance()))
        os.system("sh /home/pi/pbl2/cron/photo_cron.sh")


watering = watering.Pomp()
watering.mode = WATEROFF_MODE

if __name__ == '__main__':
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port=port, keepalive=60)

    client.loop_start()
  # print(START_SEC)

    while True:
        if watering.mode == WATERON_MODE:
            DELTA_SEC = datetime.datetime.today() - START_SEC
#           print(DELTA_SEC)
            if DELTA_SEC.total_seconds() > water_limit:
                watering.mode = WATEROFF_MODE
                watering.switch()
                print("time is over")
        time.sleep(0.5)