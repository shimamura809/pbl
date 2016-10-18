from time import sleep
import paho.mqtt.client as mqtt
import random
from datetime import datetime

host = '127.0.0.1'
port = 1883
topic = 'test/test/test'

def tempature():
	tmp1 = random.random()
	return tmp1

def moisture():
	tmp2 = random.random()
	return tmp2

# インスタンス作成時に protocol v3.1.1 を指定します
client = mqtt.Client(protocol=mqtt.MQTTv311)

client.connect(host, port=port, keepalive=60)

tmp_list = []

#for i in range(3):
#   if i == 0:
#    	tmp_list.append(tempature())
#    elif i == 1:
#    	tmp_list.append(moisture())
#    else:
#    	tmp_list.append('aaaaaa')
#client.publish(topic, str({'tempature':tmp_list[0],'moisture':tmp_list[1],'test':tmp_list[2]}))
#sleep(0.2)
for i in range(4):
    if i == 0:
        client.publish('test/test/tempature', str(tempature()))
    elif i == 1:
        client.publish('test/test/moisture', str(moisture()))
    elif i == 2:
        client.publish('test/test/datetime', str(datetime.now()))
    else:
        client.publish('test/test/test', 'aaaaa')
sleep(0.2)

client.disconnect()