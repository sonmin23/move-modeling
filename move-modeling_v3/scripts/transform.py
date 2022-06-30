from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from pyproj import Transformer

"""
좌표계 변환 프로그램.
WGS84 -> TM
TM -> WGS84
"""

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

    def do_some_business_logic(self) -> None:

        """
        Transform(Stragtegy) 개체에 위임.
        """
        # 좌표 값 35.110171834905344, 129.0936669487969 1145411.4096030626, 1680304.7544167184
        local1 = [129.0936669487969, 35.110171834905344]
        local2 = [1145430.374580664+800, 1680302.408936668-1050]
        local3 = [0,0]
        local4 = []
        local5 = []
        print([local1, local2, local3, local4, local5])
        result = self.transform.do_transform([local1, local2, local3])
        print(result)
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
    TM -> WGS84로 변환.    TM = 5181   #TM EPSG
    WGS = 4326  #WGS EPSG
    """
    def do_transform(self, data: List) -> List:
        transformer = Transformer.from_crs(5178, 4326, always_xy=True)
        wgs = [pt for pt in transformer.itransform(data)]
        return wgs

class TmTransform(Transform):
    """
    WGS84 -> TM으로 변환.
    """
    def do_transform(self, data: List) -> List:
        save = []
        transformer = Transformer.from_crs(4326, 5178, always_xy=True)
        tm = [pt for pt in transformer.itransform(data)]
        save += [0, 0, tm[1][0]-tm[0][0], tm[1][1]-tm[0][1], tm[2][0]-tm[0][0], tm[2][1]-tm[0][1]] # loc1(0,0) 기준으로 잡음
        tm += [save]
        return tm


if __name__ == "__main__":
    """
    TEST CODE
    """
    coordinate = Coordinate(WgsTransform())
    coordinate.do_some_business_logic()
    print()