from paho.mqtt import client as mqtt_client
import pygame
from pyproj import Transformer
import time
import json
import math
import deu_transform as tr
import json_parsing as deu_json
import sys
import threading
import os
from os.path import dirname

broker = '127.0.0.1'
port = ''
topic = ''
# generate client ID with pub prefix randomly
# client_id = f'python-mqtt-{random.randint(0, 100)}'
username = ''
password = ''

person = list()
vehicle = list()
field=list()
pos=list()
roadrange=list()
check_pos = list()
global_tm = list()
bluecolor=("ETC001","HD0001","HD0002","HD0003","HD0004","HD0005","HD0006","HD0007","HD0008")
VIEWSIZE = 1

color = (255, 255, 255)

transformer = Transformer.from_crs(4326, 5181, always_xy=True)

class Data: 
    xpoint = list
    ypoint = list
    time = 0

    def __init__(self, color, id): 
        self.color = color
        self.id = id

    def input_list(self, x, y):
        self.xpoint.append(x)
        self.ypoint.append(y)

    def check_time(self):
        self.time = time.perf_counter()

class Location_KNUT: 

    def __init__(self, latitude, longitude, velocity, time, direction, altitude, equ_no, dev_id):
        self.latitude = latitude
        self.longitude = longitude
        self.velocity = velocity
        self.time = time
        self.direction =direction
        self.altitude = altitude
        self.equ_no = equ_no
        self.dev_id = dev_id

def connect_mqtt(i) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.username_pw_set(username[i], password[i])
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def acceptC(): 
    thr=threading.Thread(target=run,args=())
    thr.Daemon=True 
    thr.start()


def acceptD():
    thr2=threading.Thread(target=delete_pos,args=())
    thr2.Daemon=True 
    thr2.start()


def subscribe(client: mqtt_client):

    def on_message(client, userdata, msg):
        global field
        global roadfield
        global person
        global vehicle
        global pos
        global color
        tm = list()

        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        json_data = json.loads(msg.payload.decode())
        if "status" in json_data:
            del pos[0:len(pos)]
            del check_pos[0:len(check_pos)]
        
        elif "qc_spreader" != json_data["message_id"]:
            json_data = json_data["data"]
            for pt in transformer.itransform([[json_data["longitude"], json_data["latitude"]]]):
                tm.append(pt[0])
                tm.append(pt[1])
        
            if json_data["equ_no"] in bluecolor:
                color = (1,0,255)
            else:
                color = (255,0,0)
            if len(pos) == 0: # 제일 처음 pos에 값을 넣는 경우
                pos.append(Data(color , json_data["dev_id"])) # 생성자를 이용하여 값을 넣는다.
                pos[0].xpoint=[] # 제일 첫 값이니까 인덱스는 0
                pos[0].ypoint=[] # x,ypoint는 리스트 형식(-> 5개까지만 출력하기 위해서)
                pos[0].input_list(abs(tm[0]-global_tm[0][0])/2, abs(tm[1]-global_tm[0][1])/2) # x,ypoint를 리스트로 넣어주는 함수
                check_pos.append(pos[0].id) # check_pos에 ["w1","p1"] 리스트 형식으로 아이디 값을 넣어줌.
            # 해당 id 값의 인덱스를 알기 위해서
            else:
                if json_data["dev_id"] not in check_pos: # st[1]-> 방금 받아온 id 값, check_pos -> pos 객체로 만든 id 값을 저장해둔 아이디 리스트
                # check_pos에 id 값이 없으면 pos에 생성자로 추가를 해줘야함.
                    check_pos.append(json_data["dev_id"]) 
                    pos.append(Data(color,json_data["dev_id"]))
                    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!",check_pos.index(json_data["dev_id"]))
                    tmp = check_pos.index(json_data["dev_id"]) # 해당 아이디를 check_pos에서 찾아서 인덱스로 저장
                    pos[tmp].xpoint=[]
                    pos[tmp].ypoint=[]
                    pos[tmp].input_list(abs(tm[0]-global_tm[0][0])/2, abs(tm[1]-global_tm[0][1])/2)
                else: # check_pos에 id 값이 있을 경우 (기존 pos객체에서 x,ypoint만 리스트 형식으로 받으면 됨)
                    tmp = check_pos.index(json_data["dev_id"])
                    pos[tmp].input_list(abs(tm[0]-global_tm[0][0])/2, abs(tm[1]-global_tm[0][1])/2)
                    if len(pos[tmp].xpoint) > 5: # 해당 아이디값의 객체에 x,ypoint가 5개 이상이면
                        pos[tmp].xpoint.pop(0) # 가장 오래된 것을 지움
                        pos[tmp].ypoint.pop(0)
                        pos[tmp].check_time()
        client.loop_stop()
    client.subscribe(topic)
    client.on_message = on_message

def delete_pos():
    while True:
        for i in range(0, len(pos)):
           if pos[i].time + 3 < time.perf_counter() and pos[i].time !=0 and len(pos[i].xpoint)!=0:
               pos[i].clear



def run():
    for i in range(len(username)):  
        client = connect_mqtt(i)
        subscribe(client)
        client.loop_forever()


def pygame_draw(clock, screen, mg_scale, pos):
    global roadfield

    for p in pos:                           # 좌표 시각화
        for point in range(0,len(p.xpoint)):
            # print("이건 시각화 xpoint", len(p.xpoint))
            pygame.draw.circle(screen, p.color, (p.xpoint[point]*VIEWSIZE,p.ypoint[point]*VIEWSIZE),3)     
    # pygame.draw.rect(screen, (0,0,255), (0,0,field[2]*VIEWSIZE,field[1]*VIEWSIZE),2)    # 이동 범위 그리기
    #for pyroad in tr.roadfield:
        # print("pyroad:", pyroad)
        #pygame.draw.lines(screen, (0,0,0), True,[[pyroad[0]*VIEWSIZE,pyroad[1]*VIEWSIZE], [pyroad[2]*VIEWSIZE,pyroad[3]*VIEWSIZE],[pyroad[4]*VIEWSIZE,pyroad[5]*VIEWSIZE],[pyroad[6]*VIEWSIZE,pyroad[7]*VIEWSIZE]], 2)     

def subrun():
    global atime
    VIEWSIZE = 1
    # 3. pygame에 사용되는 전역변수 선언
    pygame.init()
    size = [400, 1050]
    screen = pygame.display.set_mode(size)
    background = pygame.image.load(dirname(os.path.dirname(os.path.abspath(__file__)))+"/static//back4.png")
    mg_scale = pygame.transform.scale(background, (400*VIEWSIZE, 1050*VIEWSIZE))
    clock = pygame.time.Clock()
 
    global start
    global field
    global person
    global vehicle        
    global pos
    global done
    global global_tm
    # field=[0, Point.C.value, Point.Y.value, 0]  # 지도 상의 (x1,y1), (x2,y2) -> 이동 가능 구역  
    done = False
    VIEWSIZE = 1
    imagetmp = 1
    while not done:
        
        clock.tick(40)                          # 초당 40번 출력       
        screen.blit(mg_scale, (0, 0))           # 좌표 0,0에 배경 그리기 
        pygame_draw(clock, screen, mg_scale, pos)
        font=pygame.font.SysFont("z",30,True,True)
        text=font.render(str(math.trunc(time.perf_counter()-start)),True,(255,255,255))
        screen.blit(text,(400,30))            
        pygame.display.update() 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == ord('c'):
                    del pos[0:len(pos)]
                    del check_pos[0:len(check_pos)]                    
            if event.type == pygame.MOUSEWHEEL: # 마우스스크롤을 했을 경우
                if event.y == -1:               # 휠을 내렸을 경우
                    if VIEWSIZE > 1:            # 최소 크기 1보다 줄이지 못함
                        VIEWSIZE -=1
                elif event.y == 1:              # 휠을 올렸을 경우
                    if VIEWSIZE < 10:           # 최대 크기 10을 넘지 못함
                        VIEWSIZE +=1             
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if imagetmp == 1:
                    global_tm = []
                    for pt in transformer.itransform([[129.0936669487969, 35.110171834905344]]):
                        global_tm.append([pt[0],pt[1]])
                elif imagetmp == 2:
                    global_tm = []
                    for pt in transformer.itransform([[129.0936669487969, 35.110171834905344]]):
                        global_tm.append([pt[0],pt[1]])
                elif imagetmp == 3:  
                    global_tm = []
                    for pt in transformer.itransform([[129.0936669487969, 35.110171834905344]]):
                        global_tm.append([pt[0],pt[1]])
                background = pygame.image.load(dirname(os.path.dirname(os.path.abspath(__file__)))+"/static//back4"".png")
                if imagetmp==3:
                    imagetmp=1
                else:
                    imagetmp+=1
                mg_scale = pygame.transform.scale(background, (400*VIEWSIZE, 1050*VIEWSIZE))
            elif event.type == pygame.QUIT: # X을 눌렀을 경우
                pygame.quit()
                quit()  
        
    pygame.quit()
    sys.exit()

def save():
    global start
    start=time.perf_counter()
    global field
    global roadrange 
    global global_tm
    
    transform = tr.Coordinate(tr.TmTransform()) # WGS -> TM
    global_list=deu_json.Parsing.global_parsing()
    transform.do_move_transform(1,global_list)               # loop 정기적 호출
    id_list = deu_json.Parsing.road_id_parsing()
    for road_id in id_list:
        roadrange+=deu_json.Parsing.road_parsing(road_id)
    transform.do_move_transform(2,roadrange)               # loop 정기적 호출
    field=tr.field
    field[1]=abs(field[3])
    field[3]=0

    for pt in transformer.itransform([[129.0936669487969, 35.110171834905344]]):
        global_tm.append([pt[0],pt[1]])

def mqtt_info_open():
    global port
    global topic
    global username
    global password
    mqtt_info_list=deu_json.mqtt_info_parsing()
    mqtt_info_port=mqtt_info_list['port']
    mqtt_info_name=mqtt_info_list['name']
    mqtt_info_id=mqtt_info_list['id']
    mqtt_info_pw=mqtt_info_list['pw']

    port=int(mqtt_info_port)
    topic=mqtt_info_name
    username=mqtt_info_id
    password=mqtt_info_pw

if __name__ == '__main__':
    deu_json.viewer_file_open()
    global_list=deu_json.Parsing.global_parsing()
    mqtt_info_open()
    save()
    acceptC()
    # acceptD()
    subrun()