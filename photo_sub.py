import paho.mqtt.client as mqtt
import datetime

host = 'localhost'
port = 1883
topic = 'AIoT/Photo/'

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe(topic+'#')


def on_message(client, userdata, msg):

    # print(msg.topic+" "+str(msg.payload))
    if msg.topic == 'AIoT/Photo/now':
        filename = "./media/now/" + datetime.datetime.today().strftime("%Y%m%d%H%M%S")+".jpg"
    else:
        filename = "./media/" + datetime.datetime.today().strftime("%Y%m%d")+".jpg"
    #outfile=open( filename , 'w')
    #outfile.write(msg.payload)
    outfile=open(filename , 'wb')
    outfile.write(msg.payload)
    print ("subscribe: " + filename)
    outfile.close



if __name__ == '__main__':
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    print(client)
    client.on_connect = on_connect
    print(on_connect)
    client.on_message = on_message
    print(on_message)
    client.connect(host, port=port, keepalive=60)
    #waiting
    client.loop_forever()
