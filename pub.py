from time import sleep
import paho.mqtt.client as mqtt
import random
import math
import datetime
import grovepi

host = '210.152.14.37'
port = 1883
topic = 'AIoT/data/'
th_sensor = 3
l_sensor = 0
m_sensor = 1

retry_limit = 10
tryspan = 1

def temperature():
    starttemp =datetime.datetime.today()
    trytemp = 0
    tmp1 = grovepi.dht(th_sensor,0) [0]
    while trytemp < retry_limit:
        if isinstance(tmp1,str) or tmp1 < 0:
            tmp1 = grovepi.dht(th_sensor,0) [0]
            trytemp += 1
            sleep(tryspan)
        else:
            return tmp1
    return "nodata"

def moisture():
    startmois =datetime.datetime.today()
    trymois = 0
    tmp2 = grovepi.analogRead(m_sensor)
    while trymois < retry_limit:
        if isinstance(tmp2,str) or tmp2 < 0:
            tmp2 = grovepi.dht(th_sensor,0) [0]
            trymois += 1
            sleep(tryspan)
        else:
            return tmp2
    return "nodata"

def illuminance():
    startill =datetime.datetime.today()
    tryill = 0
    tmp3 = grovepi.analogRead(l_sensor)
    while (datetime.datetime.today() - startill).total_seconds() < retry_limit:
        if isinstance(tmp3,str) or tmp3 < 0:
            tmp3 = grovepi.dht(th_sensor,0) [0]
            tryill += 1
            sleep(tryspan)
        else:
            return tmp3
    return "No data"

client = mqtt.Client(protocol=mqtt.MQTTv311)

client.connect(host, port=port, keepalive=60)

d = datetime.datetime.today()
dstr = d.strftime('%Y-%m-%d %H:%M:%S')

client.publish(topic, "datetime:"+dstr+"/temperature:"+str(temperature())+"/moisture:"+str(moisture())+"/illuminance:"+str(illuminance()))
sleep(0.2)

client.disconnect()
