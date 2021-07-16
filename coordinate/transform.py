from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from enum import Enum
from pyproj import Transformer
import numpy as np
import folium

import coordinate as py

person=list()   #작업자 리스트
vehicle=list()  #이동장비 리스트
lwgs = list()
vwgs = list()

"""
좌표계 변환 프로그램.
WGS84 -> TM
TM -> WGS84
"""

class Epsg(Enum):
    TM = 5174
    WGS = 4326

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

        local1 = [x+385436.34396850807, y+184725.65200131526+2.953922261716798]

        # local1 = [385436.34396850807, 184725.65200131526]
        # local2 = [385470.18479922, 184912.4034081155]
        # local3 = [385554.5004668975, 184904.913774751]
        # local4 = [385481.9058922854, 184722.69807905355]
        # local1 = [129.035568, 35.144610]
        # local2 = [129.035981, 35.146286]
        # local3 = [129.036904, 35.146203]
        # local4 = [129.036067, 35.144575]

        result= self.transform.do_transform([local1])
        result = [element for array in result for element in array]
        lwgs.append(result)
        # ...
    def do_vehicle(self, x, y) -> None:

        """
        Transform(Stragtegy) 개체에 위임.
        """
        # 좌표 값

        local1 = [x+385436.34396850807, y+184725.65200131526+2.953922261716798]
        # local1 = [385436.34396850807, 184725.65200131526]
        # local2 = [385470.18479922, 184912.4034081155]
        # local3 = [385554.5004668975, 184904.913774751]
        # local4 = [385481.9058922854, 184722.69807905355]
        # local1 = [129.035568, 35.144610]
        # local2 = [129.035981, 35.146286]
        # local3 = [129.036904, 35.146203]
        # local4 = [129.036067, 35.144575]

        
        result= self.transform.do_transform([local1])
        result = [element for array in result for element in array]
        vwgs.append(result)
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
    def do_transform(self, data: List) -> List:
        save = []
        transformer = Transformer.from_crs(Epsg.WGS.value, Epsg.TM.value, always_xy=True)
        tm = [pt for pt in transformer.itransform(data)]
        save += [0, 0, tm[1][0]-tm[0][0], tm[1][1]-tm[0][1], tm[2][0]-tm[0][0], tm[2][1]-tm[0][1], tm[3][0]-tm[0][0], tm[3][1]-tm[0][1]] # loc1(0,0) 기준으로 잡음
        tm += [save]
        return tm

if __name__ == "__main__":
    """
    TEST CODE
    """
    person,vehicle = py.start()
    coordinate = Coordinate(WgsTransform())
    print("tm")
    for i in range(len(person)):    # 0부터 객체 person의 길이만큼 반복
        coordinate.do_person(person[i].x1, person[i].y1)

    for i in range(len(vehicle)):    # 0부터 객체 person의 길이만큼 반복
        coordinate.do_vehicle(vehicle[i].x1, vehicle[i].y1)

    lines = [[35.144610, 129.035568],
    [35.146203, 129.036904]]

    center = [lwgs[i][1],lwgs[i][0]]
    m = folium.Map(location=center, zoom_start=10)

    folium.Rectangle(
        bounds = lines,
        tooltip = 'Rectangle',
        color = "yellow"
    ).add_to(m)

    print([lwgs[0][1], lwgs[1][0]])
    for i in range(len(lwgs)):
        
        folium.Circle(
            location = [lwgs[i][1],lwgs[i][0]],
            radius = 0.01
        ).add_to(m)
    for i in range(len(vwgs)):
        
        folium.Circle(
            location = [vwgs[i][1],vwgs[i][0]],
            radius = 0.01,
            color = "red"
        ).add_to(m)

    m.save('./map1.html')
    py.pystart()