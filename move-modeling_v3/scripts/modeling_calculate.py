from haversine import haversine
from math import *

"""
두 좌표 사이의 속도 구하기
Parameters: mode(km or m), src(lat, lon), dest(lat, lon), sec
Return: velocity
"""
def velocity_two_coordinates(mode, src, dest, sec):
    if mode == 'km':
        return haversine(src, dest, unit = 'km')/(sec/3600)
    elif mode == 'm':
        return haversine(src, dest, unit = 'm')/sec
    else:
        return 0

"""
두 좌표 사이의 방향 구하기
Parameters: src(lat, lon), dest(lat, lon)
Return: direction
"""
def direction_two_coordinates(src, dest):
    phi1 = src[0] * pi / 180; 
    phi2 = dest[0] * pi / 180; 
    lambda1 = src[1] * pi / 180; 
    lambda2 = dest[1]  * pi / 180; 
    y = sin(lambda2 - lambda1) * cos(phi2)
    x = cos(phi1) * sin(phi2) - sin(phi1) * cos(phi2) * cos(lambda2 - lambda1)
    theta = atan2(y, x)
    direction = (theta * 180 / pi + 360) % 360
    return direction

"""
소수점 이하 버리기
Parameters: num, n -> num: float 형식, n: 소수점 뒤 자리
Return: float(temp)
"""
def truncate(num,n):
    temp = str(num)
    for x in range(len(temp)):
        if temp[x] == '.':
            try:
                return float(temp[:x+n+1])
            except:
                return float(temp)      
    return float(temp)
    
#if __name__ == '__main__':
#    src =(float(35.098484), float(129.095151)) # (lat, lon) 
#    dest = (float(35.098485), float(129.09515))
#
#    print(velocity_two_coordinates('km', src, dest, 0.5))
#    print(direction_two_coordinates(src, dest))
