1. 개발 환경
* OS : Windows 10
* Programming Language : Python3.9.7, Python3.9.10
* IDE : Visual Code Studio

2. 도커 환경
* 사용 이미지: eclipse-mosquitto:2.0.11
* 포트 번호: 9884
* VA(한국교통대학교) username/passwd : user10/user10
* WK(한양대학교) username/passwd : user16/user16
* deu username/passwd : deu01/deu01
* 추가 username/passwd : user13/user13

3. 도커 이미지 사용 방법
docker run -it -d -p 9884:9884 --name mosquitto qwe5908/mqtt

MQTT 사용자 생성 및 비밀번호 설정
* 첫 사용자 생성 옵션: -c / 추가 사용자 생성 옵션: -b

> docker exec -it mosquitto sh
# mosquitto_passwd -c /mosquitto/config/pwfile <username>
# mosquitto_passwd -b /mosquitto/config/pwfile <username> <passwd>
# vi mosquitto-no-auth.conf

mosquitto-no-auth.conf 파일 수정

listener 9884
allow_anonymous false
password_file /mosquitto/config/pwfile

docker 컨테이너 restart

> docker restart mosquitto

4. 실행 방법

> python scripts/pub_mqtt_v3.py [senario name ]/[senario number] mqtt
* senario number 입력(1~13)
예) python scripts/pub_mqtt_v3.py VA1/1 mqtt

5. 사용 패키지
certifi==2021.10.8
dnspython==2.1.0
keyboard==0.13.5
numpy==1.21.4
paho-mqtt==1.6.1
pygame==2.1.0
pyproj==3.3.0
python-etcd==0.4.5
Shapely==1.8.0
urllib3==1.26.7