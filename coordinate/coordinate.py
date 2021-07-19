import random
from math import *
from enum import Enum
import math
import pygame # 1. pygame 선언

person=list()   #작업자 리스트
vehicle=list()  #이동장비 리스트
note=list()
field=list()
num=list()
pygame.init() # 2. pygame 초기화
step=1
class Point(Enum):
    Y = 14.508216601563618  # 0,0 기준 y값
    C = 103.16860620910302

class Move: 
    """
    부모 클래스
    자식 클래스 -> 작업자 클래스, 이동장비 클래스
    """
    def __init__(self, time, x1, y1, speed, x2, y2):    # 시간, 시작좌표(x1, y1), 속도, 도착좌표(x2, y2)
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
        self.speed=speed
        self.time=time

    def euclidean_distance(self,x,y):                   # tm 거리 구하는 함수
        return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

    def location_assign():
        """
        지도 상의 작업장, 이동장비 loc1, loc2을
        랜덤 값으로 정해줌.
        """
        global field
        field=[0, Point.C.value, Point.Y.value, 0]  # 지도 상의 (x1,y1), (x2,y2) -> 이동 가능 구역  

        while True:
            x1=random.uniform(field[0],field[2]+1)
            y1=random.uniform(field[1],field[3]+1)
            x2=random.uniform(field[0],field[2]+1)
            y2=random.uniform(field[1],field[3]+1)

            # 중복 제거를 위한 조건문.
            if x1!=x2:
                if y1!=y2:
                    if x1>x2:
                        x1,x2=x2,x1
                    if y1>y2:
                        y1,y2=y2,y1
                    break
        note=[x1,y1,x2,y2]
        return x1,y1,x2,y2

class Person(Move):
    """
    작업자 클래스
    """
    def __init__(self, name, time, x1, y1, speed, x2, y2):  # 이름, 시간, 시작좌표(x1, y1), 속도, 도착좌표(x2, y2)
        Move.__init__(self, time, x1, y1, speed, x2, y2)    # 부모 클래스 생성자 호출
        self.name=name

    def location(self): # 이동할 좌표구하는 함수
        time = 0
        # self.x1=5
        # self.y1=5
        # self.x2=30
        # self.y2=30
        # self.speed=1
        c=0
        loc1=[self.x1,self.y1]
        loc2=[self.x2,self.y2]
        r = self.euclidean_distance(loc1, loc2)
        while True:
            r = r-self.speed
            radian = math.atan2(loc2[1]-loc1[1], loc2[0]-loc1[0])
            loc1[0] = loc2[0] - r * math.cos(radian)
            loc1[1] = loc2[1] - r * math.sin(radian)
            time += step

            if loc1> loc2:
                loc1 = loc2
                person.append(Person(self.name, time, loc1[0],loc1[1], self.speed, loc2[0], loc2[1]))
                break
            person.append(Person(self.name, time, loc1[0], loc1[1], self.speed, loc2[0], loc2[1]))

class Vehicle(Move):
    """
    이동장비 클래스
    """
    def __init__(self, name, time, x1, y1, speed, x2, y2):  # 이름, 시간, 시작좌표(x1, y1), 속도, 도착좌표(x2, y2)
        Move.__init__(self, time, x1, y1, speed, x2, y2)    # 부모 클래스 생성자 호출
        self.name=name

    def location(self): # 이동할 좌표구하는 함수
        time = 0
        loc1=[self.x1,self.y1]
        loc2=[self.x2,self.y2]
        r = self.euclidean_distance(loc1, loc2)
        while True:
            r = r-self.speed
            radian = math.atan2(loc2[1]-loc1[1], loc2[0]-loc1[0])   # 역 탄젠트 계산을 통해 radian을 구한다
            loc1[0] = loc2[0] - r * math.cos(radian)
            loc1[1] = loc2[1] - r * math.sin(radian)
            time += step
            if loc1> loc2:
                loc1 = loc2
                vehicle.append(Vehicle(self.name, time, loc1[0],loc1[1], self.speed, loc2[0], loc2[1]))
                break
            vehicle.append(Vehicle(self.name, time, loc1[0], loc1[1], self.speed, loc2[0], loc2[1]))

class InputOut():   # 입출력 클래스
    def input(self):    # 입력 함수
        global num
        num = [0, 0]
        num[0], num[1] = map(int, input("작업자, 차량:").split())
        return num

    def output(self):   # 출력 함수
        time = 0
        person_cnt = 0
        vehicle_cnt = 0
        while True:   
            for i in range(len(person)):    # 0부터 객체 person의 길이만큼 반복
                if time == person[i].time:
                    print(person[i].name, person[i].time, person[i].x1, person[i].y1)
                    person_cnt+=1
                    
            for i in range(len(vehicle)):   # 0부터 객체 vehicle의 길이만큼 반복 
                if time == vehicle[i].time:
                    print(vehicle[i].name, vehicle[i].time, vehicle[i].x1, vehicle[i].y1)
                    vehicle_cnt+=1
            time+=step   
            if(person_cnt==len(person) and vehicle_cnt==len(vehicle)):  # 전부 출력했을 경우 종료
                break  
def to_pygame(coords, height):
    """Convert coordinates into pygame coordinates (lower-left => top left)."""
    return coords[0], height - coords[1]
def pystart():
        # 3. pygame에 사용되는 전역변수 선언

    WHITE = (255, 255, 255)
    size = [400, 400]
    screen = pygame.display.set_mode(size)
    background = pygame.image.load('back3.png')
    mg_scale = pygame.transform.scale(background, (400, 400))

    done = False
    clock = pygame.time.Clock()

    # 4. pygame 무한루프
    def runGame():

        person_cnt = 0
        vehicle_cnt = 0    
        time=1
        pos=[]
        note2=[field[0],field[1],field[2]-field[0],field[3]-field[1]]
        print('이거',field[0],field[1],field[2],field[3])
        global done
        done = False
        while not done:
        
            clock.tick(10)
            screen.blit(mg_scale, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done=True

            ############################
            # 여기에 도형을 그리세요 
            ############################
            for i in range(len(person)):
                if time > len(person):
                    break            
                if time == person[i].time:
                    x,y = to_pygame([person[i].x1,person[i].y1],Point.C.value)
                    pos.append([x*3,y*3,(0,0,255)])   #파랑
                    person_cnt+=1
            for i in range(len(vehicle)):
                if time > len(vehicle):
                    break
                if time == vehicle[i].time:
                    x, y = to_pygame([vehicle[i].x1,vehicle[i].y1],Point.C.value)
                    pos.append([x*3, y*3,(255,0,0)]) #빨강
                    vehicle_cnt+=1

            for p in pos:
                pygame.draw.circle(screen, p[2], (p[0],p[1]),2)         

            print(person_cnt,len(person),vehicle_cnt,len(vehicle))
            if(person_cnt==len(person)-num[0] and vehicle_cnt==len(vehicle)-num[1]):  # 전부 출력했을 경우 종료
                while not done:
                    for event in pygame.event.get():# User did something
                        if event.type == pygame.QUIT:# If user clicked close
                            print("끝")
                            done=True  

            pygame.draw.rect(screen, (0,0,255), (note2[0]*3,note2[1]*3,note2[2]*3,note2[3]*3),2)
            pygame.display.update()
            time+=step

    runGame()
    pygame.quit()
def start():

    """
    Test Code
    """
    time = pi = vi = 0 # time -> 초당 지난 시간  pi, vi -> ID
    in_output = InputOut() 
    num = in_output.input() # 작업자, 이동장비의 수 입력
    
    for i in range(num[0]):
        pi += 1 # 작업자의 ID
        x1,y1,x2,y2=Move.location_assign() # 작업자의 loc1, loc2 값
        speed1=random.uniform(0.277778,1.38889) # speed1 -> 작업자의 이동 속도
        p = Person('p'+str(pi),time,x1,y1,speed1,x2,y2) # 작업자 객체 생성
        person.append(p) # person에 생성한 객체를 추가(list 형식)
        p.location() # 초당 이동 거리에 대한 메소드

    for i in range(num[1]):
        vi += 1 # 이동장비의 ID
        x1,y1,x2,y2=Move.location_assign() # 이동장비의 loc1, loc2 값
        speed2=random.uniform(2.77778,8.33333) # speed2 -> 이동장비의 이동 속도
        v=Vehicle('v'+str(vi),time,x1,y1,speed2,x2,y2) # 이동장비 객체 생성
        vehicle.append(v) # vehicle에 생성한 객체를 추가(list 형식)
        v.location() # 초당 이동 거리에 대한 메소드
    in_output.output() # 작업자, 이동장비 값 출력
    return person, vehicle