from dataclasses import field
import random
from paho.mqtt import client as mqtt_client
import deu_coordinate as cor
import deu_transform as tr
import time

broker = '127.0.0.1'
port = 1883
topic = "python/mqtt"
username=['test','admin']
password=['test','admin'] 

client_id= list() # sub 받는 ID
person=list()     # 작업자
vehicle=list()    # 이동수단
field=list()      # 이동범위
num=list()        # 작업자, 이동수단 입력 수 

def connect_mqtt(i):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client_id.append(f'python-mqtt-{random.randint(0, 1000)}') #ID 생성
    client = mqtt_client.Client(client_id[i]) # client 지정
    client.username_pw_set(username[i], password[i]) # user id, pw
    client.on_connect = on_connect # 연결
    client.connect(broker, port)
    return client

def person_publish(client,k): # 작업자 publish
    msg_count = person[k].time, person[k].name, person[k].x1, person[k].y1, person[k].speed, person[k].x2, person[k].y2
    msg = f"person:{msg_count}" # 작업자의 정보를 msg에 저장
    result = client.publish(topic, msg) 
    # result: [0, 1]
    status = result[0]
    if status == 0: # 보내는 값 출력
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def vehicle_publish(client,k): # 이동수단 publish
    msg_count = vehicle[k].time, vehicle[k].name, vehicle[k].x1, vehicle[k].y1, vehicle[k].speed, vehicle[k].x2, vehicle[k].y2
    msg = f"vehicle:{msg_count}" # 이동수단의 정보를 msg에 저장
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0: # 보내는 값 출력
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def run():
    global step     # pub 할 때 delay 시간
    global person   # 작업자
    global vehicle  # 이동수단
    global num      # 작업자, 이동수단 입력 수 
    global field    # 이동범위

    for i in range(len(username)):  
        num = person = vehicle = [] # 변수 초기화

        client=connect_mqtt(i) # mqtt 연결
        client.loop_start()

        real_time=0            # pub 할 때 보내는 시간
        step=cor.stepgo()      # step 반환

        transform = tr.Coordinate(tr.TmTransform()) # WGS -> TM
        transform.do_move_transform()               # loop 정기적 호출
        person,vehicle,num = cor.run(tr.field)      # deu_coordinate -> 작업자, 이동장비 생성 후 -> map 출력
        field=cor.tmgo()                            # field 값 리턴

        msg_count = field+num                       
        msg = f"field:{msg_count}"
        client.publish(topic, msg) 

        while True:
            start=time.perf_counter()              # 코드 실행 시간

            for k in range(len(person)):           # person 발행
                if real_time == person[k].time:
                    person_publish(client,k)

            for k in range(len(vehicle)):           # vehicle 발행
                if real_time == vehicle[k].time:
                    vehicle_publish(client,k)

            real_time+=step                         # pub 할 때 보내는 시간
            delay_time=step-(time.perf_counter()-start)  # delay_time -> 
                                                         # pub할 때 원하는 delay 시간 = 코드 실행 시간 - 시작 시간
            # print("time :", a, " perf_counter :",b) 테스트용// 나중에 변수 a 이걸로 수정 step-(time.perf_counter()-start)
            time.sleep(delay_time)
        
if __name__ == '__main__':
    run()