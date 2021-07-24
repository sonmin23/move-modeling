import ast
from enum import Flag
from paho.mqtt import client as mqtt_client
import re
import pygame

broker = '127.0.0.1'
port = 1883
topic = "python/mqtt"
username = 'test'
password = 'test'
person = list()
vehicle = list()
field=list()
pos=list()
VIEWSIZE = 1
flag = 0
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
        global pos
        global start
        global flag
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.payload.decode().find('person:')==0:
            st = re.search('person:((.*))', msg.payload.decode()).group(1)  # person:을 가지고 있는 메세지 확인
            st = ast.literal_eval(st)                       # 문자열을 리스트 형태로 변경
            person.append(st)
            pos.append([st[2],field[1]-st[3],(0,0,255)])    # 좌표 추가
        elif msg.payload.decode().find('vehicle:')==0:
            st = re.search('vehicle:((.*))', msg.payload.decode()).group(1)
            st = ast.literal_eval(st)
            vehicle.append(st)
            pos.append([st[2],field[1]-st[3],(255,0,0)])
        elif msg.payload.decode().find('field:')==0:
            st = re.search('field:((.*))', msg.payload.decode()).group(1)
            st = ast.literal_eval(st)
            field=st
        elif msg.payload.decode().find('finish') == 0:
            flag = 1
        client.loop_stop()
        subrun()
    client.subscribe(topic)
    client.on_message = on_message
    
def subrun():
    # 3. pygame에 사용되는 전역변수 선언
    pygame.init()
    size = [400, 400]
    screen = pygame.display.set_mode(size)
    background = pygame.image.load('back3.png')
    mg_scale = pygame.transform.scale(background, (400*VIEWSIZE, 400*VIEWSIZE))
    clock = pygame.time.Clock()

    # 4. pygame 무한루프
    def runGame():
        global field
        global person
        global vehicle        
        global pos
        global VIEWSIZE   
        global done
        # field=[0, Point.C.value, Point.Y.value, 0]  # 지도 상의 (x1,y1), (x2,y2) -> 이동 가능 구역  
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEWHEEL: # 마우스스크롤을 했을 경우
                    if event.y == -1:               # 휠을 내렸을 경우
                        if VIEWSIZE > 1:            # 최소 크기 1보다 줄이지 못함
                            VIEWSIZE -=1
                    elif event.y == 1:              # 휠을 올렸을 경우
                        if VIEWSIZE < 10:           # 최대 크기 10을 넘지 못함
                            VIEWSIZE +=1                        
                elif event.type == pygame.QUIT: # X을 눌렀을 경우
                    pygame.quit()
                    quit()
            clock.tick(40)                          # 초당 40번 출력       
            screen.blit(mg_scale, (0, 0))           # 좌표 0,0에 배경 그리기     

            for p in pos:                           # 좌표 시각화
                pygame.draw.circle(screen, p[2], (p[0]*VIEWSIZE,p[1]*VIEWSIZE),2)  
            done=True
            pygame.draw.rect(screen, (0,0,255), (0,0,field[2]*VIEWSIZE,field[1]*VIEWSIZE),2)    # 이동 범위 그리기
            pygame.display.update()

            if flag == 1:                           # finish를 받았을 경우 flag == 1 # 종료를 하기 위해
                while done:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: # X을 눌렀을 경우
                            pygame.quit()
                            quit()

    runGame()

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()

    