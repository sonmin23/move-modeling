from contextlib import nullcontext
import random
import paho.mqtt.client as mqtt_client
# from paho import client as mqtt_client
import time
import json
import datetime as dt
import os
from os.path import dirname
import sys
from enum import Enum
import modeling_calculate
import threading
import logging
import datetime

broker = '127.0.0.1'
client_id= list() # sub 받는 ID
step=0.1
current_time=dt.datetime.utcnow()
wearable_location_ID=("ETC001","HD0001","HD0002","HD0003","HD0004","HD0005","HD0006","HD0007","HD0008")
location_ID=("YT375","YT376","YT377","RS501", "YT322", "YT370", "YT382","YT327", "YT391", "YT347","YT378", "YT348","TC202","YT344",
            "YT317","YT318","YT358","YT356","YT343","YT342","YT360","YT390")
qc_spreader_ID=("CC111","CC101", "CC102", "CC103", "CC105", "CC114", "CC115")
tc_spreader_ID=("TC217")
Location_KNUT_ID=("YT395","RS510","TC223","RS504","TH564","TC221","YT328","TH564",
                "YT351","ET358","ET328")
mod = sys.modules[__name__]
foldername = ""

def client_filename(i, filename):
    f = open(filename,'r')
    line=f.readline()
    line=line.split('|')
    topic=line[0]
    port=int(line[1])
    username=line[2]
    password=line[3]

    client=connect_mqtt(i, username, password, port) # mqtt 연결
    client.loop_start() 
    return client, f, topic


def connect_mqtt(i, username, password, port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client_id.append(f'python-mqtt-{random.randint(0, 1000)}') #ID 생성
    client = mqtt_client.Client(client_id[i]) # client 지정
    client.username_pw_set(username, password) # user id, pw
    client.on_connect = on_connect # 연결
    client.connect(broker, port)
    return client

def data_publish_mqtt(client,k, topic, data):
    global current_time
    msg_count={
        "message_id":"location",
        "data":{
                "latitude" : data[k][1],
                "longitude" : data[k][2],
                "altitude" : int(data[k][5]),
                "velocity" : data[k][6],
                "direction" : round(int(float(data[k][7]))),
                "time" : (dt.datetime.utcnow()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                "equ_no" : data[k][3],
                "dev_id" : data[k][4]
        }
    }

    msg = f"{msg_count}"
    msg = json.dumps(msg_count)
    result = client.publish(topic, msg)
    status = result[0]
    print(topic)
    # if status == 0: # 보내는 값 출력
    #     print(f"Send `{msg}` to topic `{topic}`")
    # else:
    #     print(f"Failed to send message to topic {topic}")   

def yt_data_publish_mqtt(client,k, topic, data):
    global current_time
    msg_count={
        "message_id":"location",
        "data":{
                "latitude" : data[k][1],
                "longitude" : data[k][2],
                "altitude" : int(data[k][5]),
                "velocity" : data[k][6],
                "direction" : round(int(float(data[k][7]))),
                "time" : (dt.datetime.utcnow()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                "position_fix" : data[k][8],# 변경필요
                "satelites" : data[k][9], # 변경필요
                "equ_no" : data[k][3],
                "dev_id" : data[k][4]
        }
    }

    msg = f"{msg_count}"
    msg = json.dumps(msg_count)
    result = client.publish(topic, msg)
    status = result[0]
    print(topic)
    # if status == 0: # 보내는 값 출력
    #     print(f"Send `{msg}` to topic `{topic}`")
    # else:
    #     print(f"Failed to send message to topic {topic}") 

def qc_data_publish_mqtt(client,k, topic, data):
    global current_time
    msg_count={
        "message_id":"qc_spreader",
        "data":{
                "time" : (dt.datetime.utcnow()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                "hoist_pos": data[k][5], #변경필요
                "trolley_pos": data[k][6],#변경필요
                "spreader_lock": data[k][7],#변경필요
                "spreader_size": data[k][8],#변경필요
                # "latitude" : data[k][1], #변경필요
                # "longitude" : data[k][2], #변경필요
                "equ_no" : data[k][3],
                "dev_id" : data[k][4]
        }
    }

    msg = f"{msg_count}"
    msg = json.dumps(msg_count)
    result = client.publish(topic, msg)
    status = result[0]
    print(topic)
    # if status == 0: # 보내는 값 출력
    #     print(f"Send `{msg}` to topic `{topic}`")
    # else:
    #     print(f"Failed to send message to topic {topic}") 

def tc_data_publish_mqtt(client,k, topic, data):
    global current_time
    msg_count={
        "message_id":"tc_spreader",
        "data":{
                "time" : (dt.datetime.utcnow()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                "hoist_pos": data[k][5], #변경필요
                "trolley_pos": data[k][6],#변경필요
                "spreader_lock": data[k][7],#변경필요
                "spreader_size": data[k][8],#변경필요
                "latitude" : data[k][1],
                "longitude" : data[k][2],
                "equ_no" : data[k][3],
                "dev_id" : data[k][4]
        }
    }

    msg = f"{msg_count}"
    msg = json.dumps(msg_count)
    result = client.publish(topic, msg)
    status = result[0]
    print(topic)
    # if status == 0: # 보내는 값 출력
    #     print(f"Send `{msg}` to topic `{topic}`")
    # else:
    #     print(f"Failed to send message to topic {topic}") 
    
def data_publish_deu(client,k, topic, data):
    global current_time

    msg_count={
        "message_id":"location",
        "data":{
                "latitude" : data[k][0],
                "longitude" : data[k][1],
                "altitude" : int(data[k][2]),
                "velocity" : round(data[k][3], 1),
                "direction" : round(int(float(data[k][4]))),
                "time" : (dt.datetime.utcnow()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                "equ_no" : data[k][6],
                "dev_id" : data[k][7]
        }
    }

    msg = f"{msg_count}"
    msg = json.dumps(msg_count)
    result = client.publish(topic, msg)
    getattr(mod, '{}'.format(data[k][8])).write(msg+"\n")
    status = result[0]
    print(topic)
    # if status == 0: # 보내는 값 출력
    #     print(f"Send `{msg}` to topic `{topic}`")
    # else:
    
    #     print(f"Failed to send message to topic {topic}")   

def yt_data_publish_deu(client,k, topic, data):
    global current_time
    msg_count={
        "message_id":"location",
        "data":{
                "latitude" : data[k][0],
                "longitude" : data[k][1],
                "altitude" : int(data[k][2]),
                "velocity" : round(data[k][3], 1),
                "direction" : round(int(float(data[k][4]))),
                "time" : (dt.datetime.utcnow()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                "position_fix" : 3,# 변경필요
                "satelites" : 8, # 변경필요
                "equ_no" : data[k][5],
                "dev_id" : data[k][6]
        }
    }

    msg = f"{msg_count}"
    msg = json.dumps(msg_count)
    result = client.publish(topic, msg)
    getattr(mod, '{}'.format(data[k][8])).write(msg+"\n")
    status = result[0]
    print(topic)
    # if status == 0: # 보내는 값 출력
    #     print(f"Send `{msg}` to topic `{topic}`")
    # else:
    #     print(f"Failed to send message to topic {topic}") 

def qc_data_publish_deu(client,k, topic, data):
    global current_time
    msg_count={
        "message_id":"qc_spreader",
        "data":{
                "time" : (dt.datetime.utcnow()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                "hoist_pos": "3070", #변경필요
                "trolley_pos": "1805",#변경필요
                "spreader_lock": "U",#변경필요
                "spreader_size": "40",#변경필요
                "latitude" : data[k][0], #변경필요
                "longitude" : data[k][1], #변경필요
                "equ_no" : data[k][5],
                "dev_id" : data[k][6]
                #"latitude" : data[k].latitude,
                #"longitude" : data[k].longitude,
        }
    }

    msg = f"{msg_count}"
    msg = json.dumps(msg_count)
    result = client.publish(topic, msg)
    getattr(mod, '{}'.format(data[k][8])).write(msg+"\n")
    status = result[0]
    print(topic)
    # if status == 0: # 보내는 값 출력
    #     print(f"Send `{msg}` to topic `{topic}`")
    # else:
    #     print(f"Failed to send message to topic {topic}") 

def tc_data_publish_deu_deu(client,k, topic, data):
    global current_time
    msg_count={
        "message_id":"tc_spreader",
        "data":{
                "time" : (dt.datetime.utcnow()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                "hoist_pos": "3070", #변경필요
                "trolley_pos": "1805",#변경필요
                "spreader_lock": "U",#변경필요
                "spreader_size": "40",#변경필요
                "latitude" : data[k][0],
                "longitude" : data[k][1],
                "equ_no" : data[k][5],
                "dev_id" : data[k][6]
        }
    }

    msg = f"{msg_count}"
    msg = json.dumps(msg_count)
    result = client.publish(topic, msg)
    getattr(mod, '{}'.format(data[k][8])).write(msg+"\n")
    status = result[0]
    print(topic)
    # if status == 0: # 보내는 값 출력
    #     print(f"Send `{msg}` to topic `{topic}`")
    # else:
    #     print(f"Failed to send message to topic {topic}") 


def file_input():
    global foldername
    fname = list()
    filenamelist = list()
    filenamelist.append('')
    filenamelist2 = list()
    filenamelist2.append(0)
    cnt=0
    mode=0
    filenames=''
    if(len(sys.argv)) > 1:
        cnt = 1
        filenames = sys.argv[1]
        for f in os.listdir(dirname(os.path.dirname(os.path.abspath(__file__)))+"/data"):
            if f[0:] not in filenamelist:
                #print(cnt,". "+f[0:])
                filenamelist.append(f[0:])
                cnt+=1
        #print(filenamelist)
        filename = filenames.split('/')
        #print(filenamelist[0])
        for folder in filenamelist:
            if '(' in folder:
                #print(folder)
                temp = folder.split('(')
                if filename[0] == temp[0]: 
                    filenames = folder+'/'+filenames.split('/')[1]
                    print(filenames)
            elif '.' in folder:
                temp = folder.split('.')
                if filename[0] == temp[0]: 
                    filenames = folder+'/'+filenames.split('/')[1]
                    print(filenames)
            else:
                if filename[0] == folder: 
                    #print(folder.split['('][0])
                    filenames = folder+'/'+filenames.split('/')[1]
        mode=sys.argv[2]
        filenames = filenames.upper()
        directory = dirname(os.path.dirname(os.path.abspath(__file__)))+"/data/"+filenames
        os.chdir(directory)

    elif(len(sys.argv)) == 1:
        cnt = 1
        for f in os.listdir(dirname(os.path.dirname(os.path.abspath(__file__)))+"/data"):
            if f[0:] not in filenamelist:
                print(cnt,". "+f[0:])
                filenamelist.append(f[0:])
                cnt+=1
        filenames = input("data filenum:")
        filenames = filenamelist[int(filenames)]
        filenames = filenames[0:]
        cnt = 1
        for f in os.listdir(dirname(os.path.dirname(os.path.abspath(__file__)))+"/data/"+filenames):
            if f[0:] not in filenamelist2:
                #print(cnt,". "+f)
                filenamelist2.append(int(f))
                #cnt+=1
        filenamelist2.sort()
        for f in filenamelist2:
            if f != 0:
                print(cnt,". ",f)
                cnt+=1
        filenames2 = input("data filenum:")
        filenames2 = filenamelist2[int(filenames2)]
        #filenames2 = filenames2[0:]
        directory = dirname(os.path.dirname(os.path.abspath(__file__)))+"/data/"+filenames+'/'+str(filenames2)
        print(directory)
        os.chdir(directory)     
        for f in os.listdir(dirname(os.path.dirname(os.path.abspath(__file__)))+"/data/"+filenames+'/'+str(filenames2)):
            fname.append(f)
        foldername = filenames+'/'+str(filenames2)
        return fname,mode   
    else:
        directory = dirname(os.path.dirname(os.path.abspath(__file__)))+"/data/"+filenames
        os.chdir(directory) 
    for f in os.listdir(dirname(os.path.dirname(os.path.abspath(__file__)))+"/data/"+filenames):
        fname.append(f)
    foldername = filenames
    return fname,mode 

def read_iot_file(fname):
    dataTemp=list()

    timeerror = 0
    for i in range(0,len(fname)):
        print(fname[i])
        file = open(fname[i],'r')
        temptime=0
        while True:
            try:
                line=str(file.readline())
                if not line: break
                jsonload=json.loads(line)
                if jsonload["data"]["equ_no"] in wearable_location_ID:
                    if 'altitude' not in jsonload['data'].keys():
                        jsonload['data']['altitude'] = '0'
                    dataTemp.append((jsonload["data"]["time"],jsonload["data"]["latitude"],jsonload["data"]["longitude"],jsonload["data"]["equ_no"],
                            jsonload["data"]["dev_id"],jsonload["data"]["altitude"],jsonload["data"]["velocity"],jsonload["data"]["direction"]))
                elif jsonload["data"]["equ_no"] in location_ID:
                    dataTemp.append((jsonload["data"]["time"],jsonload["data"]["latitude"],jsonload["data"]["longitude"],jsonload["data"]["equ_no"],
                            jsonload["data"]["dev_id"],jsonload["data"]["altitude"],jsonload["data"]["velocity"],jsonload["data"]["direction"],
                            jsonload["data"]["position_fix"],jsonload["data"]["satelites"]))
                elif jsonload["data"]["equ_no"] in qc_spreader_ID:
                    print('a')
                    if jsonload["data"].get("spreader_lock") is not None:
                        print('3')
                        dataTemp.append((jsonload["data"]["time"]," "," ",jsonload["data"]["equ_no"],jsonload["data"]["dev_id"],jsonload["data"]["hoist_pos"],
                                jsonload["data"]["trolley_pos"],jsonload["data"]["spreader_lock"],jsonload["data"]["spreader_size"]))
                    else:
                        print('4')
                        dataTemp.append((jsonload["data"]["time"],jsonload["data"]["latitude"],jsonload["data"]["longitude"],jsonload["data"]["equ_no"],
                                jsonload["data"]["dev_id"],jsonload["data"]["altitude"],jsonload["data"]["velocity"],jsonload["data"]["direction"],
                                jsonload["data"]["position_fix"],jsonload["data"]["satelites"]))

                elif jsonload["data"]["equ_no"] in tc_spreader_ID:
                    dataTemp.append((jsonload["data"]["time"],jsonload["data"]["latitude"],jsonload["data"]["longitude"],jsonload["data"]["equ_no"],
                            jsonload["data"]["dev_id"],jsonload["data"]["hoist_pos"],jsonload["data"]["trolley_pos"],
                            jsonload["data"]["spreader_lock"],jsonload["data"]["spreader_size"]))
                elif jsonload["data"]["equ_no"] in Location_KNUT_ID:
                    if jsonload["data"].get("position_fix") is not None:   
                        dataTemp.append((jsonload["data"]["time"],jsonload["data"]["latitude"],jsonload["data"]["longitude"],jsonload["data"]["equ_no"],
                                jsonload["data"]["dev_id"],jsonload["data"]["altitude"],jsonload["data"]["velocity"],jsonload["data"]["direction"],
                                    jsonload["data"]["position_fix"],jsonload["data"]["satelites"]))  
                    else:                                       
                        dataTemp.append((jsonload["data"]["time"],jsonload["data"]["latitude"],jsonload["data"]["longitude"],jsonload["data"]["equ_no"],
                                    jsonload["data"]["dev_id"],jsonload["data"]["altitude"],jsonload["data"]["velocity"],jsonload["data"]["direction"])) 
            except:
                pass
            if temptime != 0:
                backtime = datetime.datetime.strptime(jsonload["data"]["time"], '%Y-%m-%dT%H:%M:%S.%f')
                intervaltime = backtime - temptime
                intervaltime = modeling_calculate.truncate(intervaltime.total_seconds(), 2)
                #print(intervaltime)
                if jsonload["data"]["equ_no"] in wearable_location_ID:
                    if intervaltime < 0.45 or intervaltime > 0.55:
                        timeerror += 1
                        logging.warning("[TIME ERROR] %s :TIME %s : %s", timeerror, intervaltime, jsonload)
                else:
                    if intervaltime < 0.15 or intervaltime > 0.25:
                        timeerror += 1
                        logging.warning("[TIME ERROR] %s :TIME %s : %s", timeerror, intervaltime, jsonload)
            temptime = datetime.datetime.strptime(jsonload["data"]["time"], '%Y-%m-%dT%H:%M:%S.%f')

    data=sorted(dataTemp,key=lambda x:x[0])  
             
    '''
    상대적인 time 구하기
    '''
    defaulttime = datetime.datetime.strptime(data[0][0], '%Y-%m-%dT%H:%M:%S.%f')
    #print(defaulttime)
    for i in range(0,len(data)):
        data[i] = list(data[i])
        backtime = datetime.datetime.strptime(data[i][0], '%Y-%m-%dT%H:%M:%S.%f')
        backtime = backtime-defaulttime
        data[i][0] = modeling_calculate.truncate(backtime.total_seconds(), 1)
        #print(data[i][0])
        data[i] = tuple(data[i])
    data= tuple(data)

    return data

def read_deu_file(fname):
    dataTemp=list()
    for i in range(0,len(fname)):
        """
        equ_no, dev_id 파일 이름에서 추출
        """  
        dataTemprange = list()
        equ_no = ""
        dev_id = ""
        split_fname = fname[i].split('_') 
        equ_no = split_fname[0]
        dev_id = split_fname[1]

        '''
        '''
        try:
            if not os.path.exists("../return"+foldername):
                os.makedirs("../return"+foldername)
        except OSError:
            print ('Error: Creating directory. ' +  "../return"+foldername)
        setattr(mod, '{}'.format(fname[i]), open("../return"+foldername+"./"+fname[i],"w"))
        f=open(fname[i],'r')

        while True:
            line = f.readline()
            if not line: break
            line=line.split(',')

            dataTemprange.append((float(line[1]),float(line[2]),12,float(line[3]),float(line[4])\
                ,line[0],equ_no,dev_id, fname[i]))


        dataTemp += dataTemprange

    data=sorted(dataTemp,key=lambda x:x[5])   

    '''
    상대적인 time 구하기
    '''
    defaulttime = datetime.datetime.strptime(data[0][5], '%Y-%m-%d %H:%M:%S.%f')
    print(type(data))
    for i in range(0,len(data)):
        data[i] = list(data[i])
        backtime = datetime.datetime.strptime(data[i][5], '%Y-%m-%d %H:%M:%S.%f')
        backtime = backtime-defaulttime
        data[i][5] = modeling_calculate.truncate(backtime.total_seconds(), 1)
        data[i] = tuple(data[i])
    data= tuple(data)

    return data      

def run_deu(data):
    global step     # pub 할 때 delay 시간
    cnt=0
    real_time=0           # pub 할 때 보내는 시간

    wearable_client=connect_mqtt(0,"user16","user16",9884)
    wearable_client.loop_start()

    location_client=connect_mqtt(1,"user16","user16",9884)
    location_client.loop_start()

    qc_spreader_client=connect_mqtt(2,"user16","user16",9884)
    qc_spreader_client.loop_start()

    tc_spreader_client=connect_mqtt(3,"user16","user16",9884)
    tc_spreader_client.loop_start()        

    location_knut_client=connect_mqtt(4,"user10","user10",9884)
    location_knut_client.loop_start()     
    while True:
        start=time.perf_counter()
        for k in range(len(data)):
            if real_time == data[k][5]:
                if data[k][6] in wearable_location_ID:
                    data_publish_deu(wearable_client,k, "wearable_location_16", data)
                    cnt+=1
                elif data[k][6] in location_ID:
                    yt_data_publish_deu(location_client,k, "location_16", data)
                    cnt+=1
                elif data[k][6] in qc_spreader_ID:
                    qc_data_publish_deu(qc_spreader_client,k, "qc_spreader_16", data)
                    data_publish_deu(location_client,k, "location_16", data)
                    cnt+=1
                elif data[k][6] in tc_spreader_ID:
                    tc_data_publish_deu_deu(tc_spreader_client,k, "tc_spreader_16", data)
                    cnt+=1
                elif data[k][6] in Location_KNUT_ID:
                    data_publish_deu(location_knut_client,k,"location_KNUT", data)
        if cnt>=len(data)-1:
            break
        real_time = code_time(start, real_time) 
    finishpub()
    
def run_mqtt(data):
    global step     # pub 할 때 delay 시간
    cnt=0
    real_time=0           # pub 할 때 보내는 시간

    wearable_client=connect_mqtt(0,"user16","user16",9884)
    wearable_client.loop_start()

    location_client=connect_mqtt(1,"user16","user16",9884)
    location_client.loop_start()

    qc_spreader_client=connect_mqtt(2,"user16","user16",9884)
    qc_spreader_client.loop_start()

    tc_spreader_client=connect_mqtt(3,"user16","user16",9884)
    tc_spreader_client.loop_start()        

    location_knut_client=connect_mqtt(4,"user10","user10",9884)
    location_knut_client.loop_start()     
    while True:
        start=time.perf_counter()
        for k in range(len(data)):
            if real_time == data[k][0]:
                if data[k][3] in wearable_location_ID:
                    data_publish_mqtt(wearable_client,k, "wearable_location_16", data)
                    cnt+=1
                elif data[k][3] in location_ID:
                    yt_data_publish_mqtt(location_client,k, "location_16", data)
                    cnt+=1
                elif data[k][3] in qc_spreader_ID:
                    if data[k][1]==" ":
                        qc_data_publish_mqtt(qc_spreader_client,k, "qc_spreader_16", data)
                        cnt+=1     
                    else:
                        data_publish_mqtt(location_client,k, "location_16", data)
                        cnt+=1     
                elif data[k][3] in tc_spreader_ID:
                    tc_data_publish_mqtt(tc_spreader_client,k, "tc_spreader_16", data)
                    cnt+=1
                elif data[k][3] in Location_KNUT_ID:
                    if len(data[k])>=9:
                        yt_data_publish_mqtt(location_client,k, "location_16", data)
                        cnt+=1     
                    else:                   
                        data_publish_mqtt(location_knut_client,k,"location_KNUT", data)
                        cnt+=1                         
        if cnt>=len(data)-1:
            break
        real_time = code_time(start, real_time) 
        
    finishpub()  

def finishpub():
    global json_data
    client=connect_mqtt(1, "deu01", "deu01", 9884) # mqtt 연결
    client.loop_start() 
    msg_count={
        "status":"finish"
    }
    msg = f"{msg_count}"
    msg = json.dumps(msg_count)
    topic = "admin"
    result = client.publish(topic, msg)    
    status = result[0]
    if status == 0: # 보내는 값 출력
        print(f"Send `{msg}` to topic `{topic}`")
        sys.exit(0) 

def code_time(start, real_time):
    global step
    real_time+=step   
    real_time = round(real_time, 6)                           # pub 할 때 보내는 시간
    test_time=time.perf_counter()-start
    delay_time=step-test_time  # delay_time -> 
    time.sleep(delay_time)
    return real_time        

if __name__ == '__main__':
    # 버전 v3
    fname,mode=file_input()
    try:
        if mode==0:
            select=int(input("1: mqtt모드 , 2: deu 모드 :"))
            if select==1:
                data=read_iot_file(fname)
                run_mqtt(data)
            elif select==2:
                data=read_deu_file(fname)
                run_deu(data)
        elif mode=="deu":
            data=read_deu_file(fname)
            run_deu(data)
        elif mode=="mqtt":
            data=read_iot_file(fname)
            run_mqtt(data)
    except KeyboardInterrupt:
        finishpub()