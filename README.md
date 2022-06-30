# move-modeling

## 1. 개발 환경
* OS : Windows 10
* Programming Language : Python3.9.7, Python3.9.10
* IDE : Visual Code Studio

## 2. 도커 환경
* 사용 이미지: eclipse-mosquitto:2.0.11
* 포트 번호: 9884
* VA(한국교통대학교) username/passwd : user10/user10
* WK(한양대학교) username/passwd : user16/user16
* deu username/passwd : deu01/deu01
* 추가 username/passwd : user13/user13

## 3. 도커 이미지 사용 방법
docker run -it -d -p 9884:9884 --name mosquitto qwe5908/mqtt

MQTT 사용자 생성 및 비밀번호 설정
* 첫 사용자 생성 옵션: -c / 추가 사용자 생성 옵션: -b

> docker exec -it mosquitto sh  
> mosquitto_passwd -c /mosquitto/config/pwfile <username>  
> mosquitto_passwd -b /mosquitto/config/pwfile <username> <passwd>  
> vi mosquitto-no-auth.conf  

mosquitto-no-auth.conf 파일 수정

listener 9884
allow_anonymous false
password_file /mosquitto/config/pwfile

docker 컨테이너 restart

> docker restart mosquitto

## 4. 실행 방법

> python scripts/pub_mqtt_v3.py [senario name ]/[senario number] mqtt
* senario number 입력(1~13)
예) python scripts/pub_mqtt_v3.py VA1/1 mqtt

## 5. 사용 패키지
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

## 6. 요구사항 목록
### 시나리오 별 이동 모델링 정보 발행
1. 원하는 시나리오의 폴더를 번호로 입력할 수 있어야 한다.
2. 터미널, vsc로 실행할 수 있어야 한다.
3. 모드(deu/mqtt mode)를 선택할 수 있어야 한다.
4. move-modeling3/data 폴더에 존재하는 가상 테스트 시나리오 폴더 목록을 볼 수 있어야 한다.
5. 특정 시나리오 폴더에 여러 개 저장해 두어 MQTT 메시지 발행할 수 있어야 한다.
6. equ_no/serial ID 정보는 파일 명에 포함될 수 있어야 한다.
7. 이동 장비/작업자의 가상 테스트 데이터를 무한대 발행할 수 있어야 한다.
8. 다수의 mqtt client에 연결 가능할 수 있어야 한다.
9. 시나리오 발행이 끝났을 때 혹은 발행이 중단 되었을 때 발행 끝을 알리는 메시지(deu01)를 발행할 수 있어야 한다.
10. 시나리오 중 특정 장비는 두 개의 토픽(qc_speader_16/location)을 발행할 수 있어야 한다.

### deu모드 
1. 동의대 가상 테스트 데이터 생성기로 생성된 파일을 읽을 수 있어야 한다.
2. 폴더에 있는 파일을 전부 읽을 수 있어야 한다.
3. 작업자/이동 장비 구분 없이 시간 순으로 정보(Gps 정보, 시간, 속도, 방향, equ_no, serial ID)를 저장할 수 있어야 한다.
4. Gps 정보와 시간 정보(1초 간격)을 이용하여 속도, 방향 정보를 계산할 수 있어야 한다.
5. 발행된 이동 모델링 정보를 mqtt 모드에 발행할 데이터 정보로 저장할 수 있어야 한다.

### mqtt모드
1. IoT통합 플랫폼 데이터로 생성된 파일을 읽을 수 있어야 한다.
2. 폴더에 있는 파일을 전부 읽을 수 있어야 한다.
3. 작업자/이동 장비 구분 없이 시간 순으로 정보(Gps 정보, 시간, 속도, 방향, equ_no, serial ID)를 저장할 수 있어야 한다.
4. 작업자/ 이동 장비 별로 주어진 각기 다른 데이터 구분하여 발행 데이터로 변환할 수 있어야 한다.

### 이동 모델링 정보 시각화
1. mqtt 토픽을 여러 개 구독할 수 있어야 한다.
2. 파이 게임에 배경 이미지(지도)를 출력할 수 있어야 한다.
3. 마우스 오른쪽 버튼 클릭 시 배경 이미지(지도)가 변경되어야 한다.
4. 변경된 배경 이미지(지도)에 맞게 전역 좌표가 변경되어야 한다.
5. TM<->WGS 좌표 간 변환을 할 수 있어야 한다.
6. 발행 받은 이동 모델링 정보 중 GPS 정보를 이용하여 화면에 이동 장비/작업자 위치를 출력할 수 있어야 한다.
7. 출력된 이동 장비/작업자는 시각화를 위하여 이전 좌표 5개를 저장할 수 있어야 한다.
8. 시나리오 발행 끝을 알리는 메시지를 발행 받았을 때 화면에 보이는 좌표를 지울 수 있어야 한다.
9. 프로그램 실행 시간이 화면에 출력할 수 있어야 한다. 
