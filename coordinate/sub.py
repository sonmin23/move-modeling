import ast
from paho.mqtt import client as mqtt_client
import coordinate as cor
import transform as tr
import re
broker = '127.0.0.1'
port = 1883
topic = "python/mqtt"
username = 'test'
password = 'test'
person = list()
vehicle = list()
field=list()
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):    
    def on_message(client, userdata, msg):
        global field
        global person
        global vehicle
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.payload.decode().find('person:')==0:
            st = re.search('person:((.*))', msg.payload.decode()).group(1)
            st = ast.literal_eval(st)
            person.append(st)
        elif msg.payload.decode().find('vehicle:')==0:
            st = re.search('vehicle:((.*))', msg.payload.decode()).group(1)
            st = ast.literal_eval(st)
            vehicle.append(st)
        elif msg.payload.decode().find('field:')==0:
            st = re.search('field:((.*))', msg.payload.decode()).group(1)
            st = ast.literal_eval(st)
            field=st
            view = tr.View()
            view.wgs_view(person,vehicle)
            view.map_view()
            cor.pyrun(person,vehicle,field)
            person=[]
            vehicle=[]
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()