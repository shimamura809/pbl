import paho.mqtt.client as mqtt
from mongoengine import *
from pymongo import *

host = '127.0.0.1'
port = 1883
topic = 'test/test'

client = MongoClient()
db = client.pbl

data_dict = {}

def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))

    #client.subscribe(topic+'/tempature')
    #client.subscribe(topic+'/moisture')
    #client.subscribe(topic+'/test')
    client.subscribe(topic+'/#')

def split_data(msg):
    tmp = str(msg.payload).split("b'")[1].split("'")[0]
    tmp = float(tmp)
    return tmp

def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))
    if msg.topic.split("test/test/")[1] == 'tempature':
        # tempature = str(msg.payload)
        # tempature = tempature.split("b'")
        # tempature = tempature[1].split("'")[0]
        # tempature = float(tempature)
        data_dict["tempature"] = split_data(msg)
        # db.test.insert({'tempature':tempature})
    elif msg.topic.split("test/test/")[1] == 'datetime':
        datetime = str(msg.payload)
        datetime = datetime.split("b'")
        datetime = datetime[1].split("'")[0]
        # moisture = float(moisture)
        data_dict["datetime"] = datetime
        # db.test.insert({'moisture':moisture})
    elif msg.topic.split("test/test/")[1] == 'moisture':
        data_dict["moisture"] = split_data(msg)
    else:
        test = str(msg.payload)
        test = test.split("b'")
        test = test[1].split("'")[0]
        data_dict["test"] = test
        # db.test.insert({'test':test})
    if len(data_dict) == 4:
        db.test.insert({"datetime":data_dict["datetime"],"tempature":data_dict["tempature"],"moisture":data_dict["moisture"],"test":data_dict["test"]})
        data_dict.clear()

if __name__ == '__main__':
    # Publisherと同様に v3.1.1を利用
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port=port, keepalive=60)
    # 待ち受け状態にする
    client.loop_forever()