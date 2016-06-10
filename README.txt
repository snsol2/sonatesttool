1. 필요한 설치 환경 및 Package
    1). "hosts"에 "<controller_IP>     controller" 추가
        : OpenStack 인증(Get Token) 후 받은 Endpoint 정보를 이용해 각 Service와 연동 할 때
          endpoint의 url 정보가 "controller"로 되어 있는 경우 등록한다.

    2). 설치 파일
       a). pip > v8.1 이상
       b). python-neutronclient
       c). python-novaclient
       d). python-glanceclient
       e). oslo.config
       f). oslo.log
