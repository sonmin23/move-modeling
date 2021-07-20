from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from enum import Enum
from pyproj import Transformer
import numpy as np
import folium
import coordinate as cor

person=list()   #작업자 리스트
vehicle=list()  #이동장비 리스트
lwgs = list()
vwgs = list()
field = []
pol=list()
"""
좌표계 변환 프로그램.
WGS84 -> TM
TM -> WGS84
"""

class Epsg(Enum):
    TM = 5174   #TM EPSG
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
        result = [element for array in result for element in array]
        lwgs.append(result)
        # ...
    def do_vehicle(self, x, y) -> None:
        """
        Transform(Stragtegy) 개체에 위임.
        """
        # 좌표 값

        local1 = [x+Point[0], y+Point[1]-Point[2]] 
        result= self.transform.do_transform([local1])
        result = [element for array in result for element in array]
        vwgs.append(result)
        # ...

    def do_move_transform(self) -> None:
        """
        Transform(Stragtegy) 개체에 위임.
        """
        # 좌표 값
        local1 = [129.033684, 35.147540]
        local2 = [129.033820, 35.146608]
        print("이동 범위 (WTS):", [local1, local2])
        result = self.transform.do_transform([local1, local2])
        print("이동 범위 (TM):", result)
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
        print(wgs)
        return wgs

class TmTransform(Transform):
    """
    WGS84 -> TM으로 변환.
    """
    def do_transform(self, data: List) -> List:
        global field
        global Point
        save = []
        transformer = Transformer.from_crs(Epsg.WGS.value, Epsg.TM.value, always_xy=True)
        tm = [pt for pt in transformer.itransform(data)]
        save += [0, 0, tm[1][0]-tm[0][0], tm[1][1]-tm[0][1]] # loc1(0,0) 기준으로 잡음
        tm += [save]
        field=tm[2]
        pol=tm[0]
        Point=(pol[0],pol[1],abs(field[3]))
        return tm

    def tmgo():
        global field
        return field

class View():
    def wgs_view_transform(self):
        coordinate = Coordinate(TmTransform())
        coordinate.do_move_transform()
        person,vehicle,num = cor.run(field)
        coordinate = Coordinate(WgsTransform())
        print("WGS 값 출력")
        for i in range(len(person)):    # 0부터 객체 person의 길이만큼 반복
            coordinate.do_person(person[i].x1, person[i].y1) #좌표 변환

        for i in range(len(vehicle)):    # 0부터 객체 person의 길이만큼 반복
            coordinate.do_vehicle(vehicle[i].x1, vehicle[i].y1) #좌표 변환


    def wgs_view(self, person,vehicle):
        coordinate = Coordinate(TmTransform())
        coordinate.do_move_transform()
        # person,vehicle = cor.run()
        coordinate = Coordinate(WgsTransform())
        print("WGS 값 출력")
        for i in range(len(person)):    # 0부터 객체 person의 길이만큼 반복
            coordinate.do_person(person[i][2], person[i][3]) #좌표 변환

        for i in range(len(vehicle)):    # 0부터 객체 person의 길이만큼 반복
            coordinate.do_vehicle(vehicle[i][2], vehicle[i][3]) #좌표 변환

    def py_view(self):
        cor.pystart()

    def map_view(self):
        lines = [[35.147540, 129.033684], [35.146608, 129.033820]] #이동 범위
        center = [35.147540, 129.033684]
        m = folium.Map(location=center, zoom_start=500)

        folium.Rectangle( #사각형으로 표시
            bounds = lines, #이동범위
            tooltip = 'Rectangle',
            color = "yellow").add_to(m)

        for i in range(len(lwgs)): #lwgs-> 작업자 WGS 이동 정보
            folium.Circle(
                location = [lwgs[i][1],lwgs[i][0]], 
                radius = 0.01
            ).add_to(m)

        for i in range(len(vwgs)): #Vwgs-> 이동수단 WGS 이동 정보
            folium.Circle(
                location = [vwgs[i][1],vwgs[i][0]],
                radius = 0.01,
                color = "red"
            ).add_to(m)

        m.save('./map1.html')
        
class TransformControll():
    def run(self):
        view = View()
        view.wgs_view_transform()
        view.map_view()
        view.py_view()

if __name__ == "__main__":
    """
    TEST CODE
    """
    controller = TransformControll()
    controller.run()