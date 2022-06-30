import json
import os
from os.path import dirname

filename = ""

class Worker: 

    def __init__(self, time, speed, waypoint, mode, num, equ_no, dev_id, name, port, id, pw):    # 시간, 시작좌표(x1, y1), 속도, 도착좌표(x2, y2)
        self.speed=speed
        self.time=time
        self.waypoint = waypoint
        self.mode = mode
        self.num = num
        self.equ_no = equ_no
        self.dev_id = dev_id
        self.name = name
        self.port = port
        self.id = id
        self.pw = pw
    
    def worker_parsing(worker_id):
        json_data = open_file()
        globals()['{}'.format(worker_id)] = json_data['{}'.format(worker_id)]
        time = json_data['{}'.format(worker_id)]["time"]
        speed = json_data['{}'.format(worker_id)]["speed"]
        routes = json_data['{}'.format(worker_id)]["routes"]
        mode = json_data['{}'.format(worker_id)]["mode"]
        num = json_data['{}'.format(worker_id)]["num"]
        equ_no = json_data['{}'.format(worker_id)]["equ_no"]
        dev_id = json_data['{}'.format(worker_id)]["dev_id"]
        name = json_data['{}'.format(worker_id)]["name"]
        port = json_data['{}'.format(worker_id)]["port"]
        id = json_data['{}'.format(worker_id)]["id"]
        pw = json_data['{}'.format(worker_id)]["pw"]
        worker = Worker(time,speed,routes,mode, num, equ_no, dev_id, name, port, id, pw)         
        return worker 


class Vehicle: 


    def __init__(self, time, speed, waypoint, mode, num, equ_no, dev_id, name, port, id, pw):    # 시간, 시작좌표(x1, y1), 속도, 도착좌표(x2, y2)
        self.speed=speed
        self.time=time
        self.waypoint = waypoint
        self.mode = mode
        self.num = num
        self.equ_no = equ_no
        self.dev_id = dev_id
        self.name = name
        self.port = port
        self.id = id
        self.pw = pw

    def worker_parsing(vehicle_id):
        json_data = open_file()
        globals()['{}'.format(vehicle_id)] = json_data['{}'.format(vehicle_id)]
        time = json_data['{}'.format(vehicle_id)]["time"]
        speed = json_data['{}'.format(vehicle_id)]["speed"]
        routes = json_data['{}'.format(vehicle_id)]["routes"]
        mode = json_data['{}'.format(vehicle_id)]["mode"]
        num = json_data['{}'.format(vehicle_id)]["num"]
        equ_no = json_data['{}'.format(vehicle_id)]["equ_no"]
        dev_id = json_data['{}'.format(vehicle_id)]["dev_id"]      
        name = json_data['{}'.format(vehicle_id)]["name"]
        port = json_data['{}'.format(vehicle_id)]["port"]
        id = json_data['{}'.format(vehicle_id)]["id"]
        pw = json_data['{}'.format(vehicle_id)]["pw"]
        vehicle = Vehicle(time,speed,routes,mode, num, equ_no, dev_id, name, port, id, pw) 
        return vehicle 

class Parsing:
    
    def __init__(self, worker_id_list, vehicle_id_list):    # 시간, 시작좌표(x1, y1), 속도, 도착좌표(x2, y2)
        self.__worker_id_list=worker_id_list
        self.__vehicle_id_list=vehicle_id_list

    def parsing():
        with open(filename) as json_file:
            json_data = json.load(json_file)

        worker_id_list = json_data["worker_id"]
        vehicle_id_list = json_data["vehicle_id"]
        parsing = Parsing(worker_id_list, vehicle_id_list)
        return parsing

    def global_parsing():
        json_data=open_file()
        global_list = json_data["global"]
        return global_list

    def road_id_parsing():
        json_data=open_file()
        road_id_list=json_data["road_id"]
        return road_id_list

    def road_parsing(road_id):
        json_data = open_file()
        road_list = json_data['{}'.format(road_id)]
        return road_list

    @property
    def worker_id_list(self):   #getter
        return self.__worker_id_list

    @property
    def vehicle_id_list(self):   #getter
        return self.__vehicle_id_list

def mqtt_info():
    with open(filename) as json_file:
        json_data = json.load(json_file)
    return str(json_data["mqtt_info"]["name"])+\
        "|"+str(json_data["mqtt_info"]["port"])+\
            "|"+str(json_data["mqtt_info"]["id"])+\
                "|"+str(json_data["mqtt_info"]["pw"])+"|\n"

def first_open_file(pathfile, filenames):
    global filename
    
    directory = dirname(os.path.dirname(os.path.abspath(__file__)))+"/json"
    
    os.chdir(directory)
    
    filename = filenames+".json"
    
    print(filename)

    with open(filename) as json_file:
        json_data = json.load(json_file)
    return json_data

def viewer_file_open():
    global filename
    directory = dirname(os.path.dirname(os.path.abspath(__file__)))+"/json"
    os.chdir(directory)
    filename = "WK_TC_02.json"

    with open(filename) as json_file:
        json_data = json.load(json_file)
    return json_data

def open_file():
    with open(filename) as json_file:
        json_data = json.load(json_file)
    return json_data

def mqtt_info_parsing():
    with open(os.path.abspath('mqtt_info.json')) as json_file:
        json_data = json.load(json_file)

    mqtt_info_list = json_data["mqtt_info"]
    return mqtt_info_list    