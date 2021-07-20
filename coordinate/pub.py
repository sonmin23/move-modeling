from dataclasses import field
import random
from paho.mqtt import client as mqtt_client
import coordinate as cor
import transform as tr
broker = '127.0.0.1'
port = 1883
topic = "python/mqtt"
username=['test','admin']
password=['test','admin'] 
client_id=list()
person=list()
vehicle=list()
field=list()
num=list()

def connect_mqtt(i):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client_id.append(f'python-mqtt-{random.randint(0, 1000)}')
    client = mqtt_client.Client(client_id[i])
    client.username_pw_set(username[i], password[i])
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def person_publish(client,k):
    msg_count = person[k].time, person[k].name, person[k].x1, person[k].y1, person[k].speed, person[k].x2, person[k].y2
    msg = f"person:{msg_count}"
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def vehicle_publish(client,k):
    msg_count = vehicle[k].time, vehicle[k].name, vehicle[k].x1, vehicle[k].y1, vehicle[k].speed, vehicle[k].x2, vehicle[k].y2
    msg = f"vehicle:{msg_count}"
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def run():
    global step
    global person
    global vehicle
    global num
    global field
    for i in range(len(username)):  
        num=[] 
        person=[]
        vehicle=[]   
        client=connect_mqtt(i)
        client.loop_start()
        person_cnt = 0
        vehicle_cnt = 0        
        time=0
        step=cor.stepgo()     
        transform = tr.Coordinate(tr.TmTransform())
        transform.do_move_transform()
        person,vehicle,num = cor.run(tr.field)
        while True:
            for k in range(len(person)):
                if time == person[k].time:
                    person_publish(client,k)
                    person_cnt+=1
            for k in range(len(vehicle)):
                if time == vehicle[k].time:
                    vehicle_publish(client,k)
                    vehicle_cnt+=1
            if(person_cnt==len(person) and vehicle_cnt==len(vehicle)):  # 전부 출력했을 경우 종료
                field=cor.tmgo()
                client=connect_mqtt(len(username)-1)
                client.loop_start()
                msg_count = field+num
                msg = f"field:{msg_count}"
                client.publish(topic, msg)                
                break                      
            time+=step
        client.loop_stop()
        
if __name__ == '__main__':
    run()