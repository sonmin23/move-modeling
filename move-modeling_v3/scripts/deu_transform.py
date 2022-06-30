from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from enum import Enum
from pyproj import Transformer
import numpy as np

globalfield = list()
person=list()   #작업자 리스트
vehicle=list()  #이동장비 리스트
lwgs = list()
vwgs = list()
road = list()
wgsroad = list()
field = []
pol=list()
"""
좌표계 변환 프로그램.
WGS84 -> TM
TM -> WGS84
"""

class Epsg(Enum):
    TM = 5181   #TM EPSG
    WGS = 4326  #WGS EPSG

Point=list()

class Coordinate():

    """
    Coordinate 인터페이스를 정의함.
    """

    def __init__(self, transform: Transform) -> None:
        self.transform = transform

    @property
    def transform(self) -> transform:
        return self._transform

    @transform.setter
    def transform(self, transform: Transform) -> None:
        self._transform = transform

class Coordinate():

    """
    Coordinate 인터페이스를 정의함.
    """

    def __init__(self, transform: Transform) -> None:
        self.transform = transform

    @property
    def transform(self) -> transform:
        return self._transform

    @transform.setter
    def transform(self, transform: Transform) -> None:
        self._transform = transform

    def do_person(self, x, y) -> None:
        """
        Transform(Stragtegy) 개체에 위임.
        """
        # 좌표 값
        local1 = [x+Point[0], y+Point[1]-Point[2]]
        result= self.transform.do_transform([local1])
        return result[0][1], result[0][0]
        # ...
    def do_vehicle(self, x, y) -> None:
        """
        Transform(Stragtegy) 개체에 위임.
        """
        # 좌표 값
        local1 = [x+Point[0], y+Point[1]-Point[2]] 
        result= self.transform.do_transform([local1])
        return result[0][1], result[0][0]
        # ...

    def do_move_transform(self, checkrange, data:list) -> list:
        """
        Transform(Stragtegy) 개체에 위임.
        """  
        # 좌표 값 
        # print("이동 범위 (WTS):", [data])
        result = self.transform.do_transform(checkrange, data)
        # print("이동 범위 (TM):", result)
        # ...


class Transform(ABC):
    """
    behavior
    """
    @abstractmethod
    def do_transform(self, data: List):
        pass


class WgsTransform(Transform):
    """
    TM -> WGS84로 변환.
    """
    def do_transform(self, data: List) -> List:
        transformer = Transformer.from_crs(Epsg.TM.value, Epsg.WGS.value, always_xy=True)
        wgs = [pt for pt in transformer.itransform(data)]
        wgs = np.round(wgs, 6)
        return wgs

class TmTransform(Transform):
    """
    WGS84 -> TM으로 변환.
    """
    def do_transform(self, checkrange, data: List) -> List:
        global road
        global field
        global roadfield
        global Point
        global globalfield
        global wgsroad

        if checkrange == 1:
            save = []
            transformer = Transformer.from_crs(Epsg.WGS.value, Epsg.TM.value, always_xy=True)
            tm = [pt for pt in transformer.itransform(data)]
            save += [0, 0, tm[1][0]-tm[0][0], tm[1][1]-tm[0][1]] # loc1(0,0) 기준으로 잡음
            globalfield = [tm[0][0], tm[0][1]] ##################################################추가
            tm += [save]
            field=tm[2]
            pol=tm[0]
            Point=(pol[0],pol[1],abs(field[3]))
            return tm
        else: 
            oddnumber = []
            evennumber = []
            oddsave = []
            evensave = []

            ##################################################################
            for i in range(0,len(data)):
                if(i % 2==0):
                    oddnumber += [[data[i][1], data[i][0]]] # loc1(0,0) 기준으로 잡음
                else:
                    evennumber += [[data[i][1], data[i][0]]] # loc1(0,0) 기준으로 잡음
            save = list(map(list.__add__, evennumber, oddnumber))
            # print("wgs folium save", save)
            for o in range(0, len(save)):
                if(o % 2==0):
                    oddsave.append(save[o])
                else:
                    evensave.append(save[o])
            wgsroad = list(map(list.__add__, oddsave, evensave))
            # print("wgs folium roadd", wgsroad)
            ###################################################################
            oddnumber = []
            evennumber = []
            oddsave = []
            evensave = []
            transformer = Transformer.from_crs(Epsg.WGS.value, Epsg.TM.value, always_xy=True)
            tm = [pt for pt in transformer.itransform(data)]
            ##################################################################
            for i in range(0,len(tm)):
                if(i % 2==0):
                    oddnumber += [[abs(tm[i][0]-globalfield[0]), abs(tm[i][1]-globalfield[1])]] # loc1(0,0) 기준으로 잡음
                else:
                    evennumber += [[abs(tm[i][0]-globalfield[0]), abs(tm[i][1]-globalfield[1])]] # loc1(0,0) 기준으로 잡음
            save = list(map(list.__add__, oddnumber, evennumber))

            # print(save)
            for o in range(0, len(save)):
                if(o % 2==0):
                    oddsave.append(save[o])
                else:
                    evensave.append(save[o])
            save = list(map(list.__add__, oddsave, evensave))
            roadfield = save;
            return save
            ###########################################################

    def tmgo():
        global field
        return field
