from time import sleep
import paho.mqtt.client as mqtt
import random
import datetime

host = '192.168.10.246'
port = 1883
topic = 'AIoT/data/'

def temperature():
	tmp1 = random.random()
	return tmp1

def moisture():
	tmp2 = random.random()
	return tmp2

def illuminance():
    tmp3 = random.random()
    return tmp3

client = mqtt.Client(protocol=mqtt.MQTTv311)

client.connect(host, port=port, keepalive=60)

d = datetime.datetime.today()
dstr = d.strftime('%Y-%m-%d %H:%M:%S')

client.publish(topic, "datetime:"+dstr+"/temperature:"+str(temperature())+"/moisture:"+str(moisture())+"/illuminance:"+str(illuminance()))

sleep(0.2)

client.disconnect()