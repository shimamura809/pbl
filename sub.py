import paho.mqtt.client as mqtt
from pymongo import *
from mail import *
import datetime

host = 'localhost'
port = 1883
topic = 'AIoT/data/'

client = MongoClient()
db = client.pbl

data_dict = {}

def on_connect(client, userdata, flags, respons_code):
    print('待機開始')

    client.subscribe(topic+'#')

def split_data(tmp_str):
    tmp = tmp_str.split("/")
    threshold = []
    threshold += db.threshold.find()
    data_dict["datetime"] = datetime.datetime.strptime(tmp[0], '%Y-%m-%d %H:%M:%S')
    data_dict["temperature"] = float(tmp[1].split("temperature:")[1])
    data_dict["moisture"] = float(tmp[2].split("moisture:")[1])
    data_dict["illuminance"] = float(tmp[3].split("illuminance:")[1])
    if db.threshold.count() != 0:
        if float(threshold[0]["threshold"]) > data_dict["moisture"]:
            mail_to_user()

def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))
    tmp_str = str(msg.payload).split("b'datetime:")[1].split("'")[0]
    split_data(tmp_str)
    print(data_dict)

    if len(data_dict) == 4:
        db.collect_data.insert({"datetime":data_dict["datetime"],"temperature":data_dict["temperature"],"moisture":data_dict["moisture"],"illuminance":data_dict["illuminance"]})
        data_dict.clear()

if __name__ == '__main__':
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port=port, keepalive=60)
    # 待ち受け状態にする
    client.loop_forever()