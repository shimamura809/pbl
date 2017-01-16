import paho.mqtt.client as mqtt

#host ="210.152.14.37"
host = "localhost"
port = 1883
topic = "#"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def order(message):
    if message == "ON":
        client.publish("test", "wateron")
    elif message == "OFF":
        client.publish("test", "wateroff")

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.connect(host, port=port, keepalive=60)
#order("ON")