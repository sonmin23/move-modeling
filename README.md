# move-modeling

## 좌표 변환

TM - EPSG : 5174

WGS - EPSG : 4326

- TM → WGS
- WGS → TM

## 이동 모델링

- 작업자, 이동수단의 초당 이동 표시
- TM - pygame으로 초당 이동 모델링 시각화
- WGS - Folium으로 지도에 이동 모델링 시각화

## MQTT

- pub: 초당 좌표 값 전송 및 지도 생성
- sub: 파이 게임에 좌표 시각화
