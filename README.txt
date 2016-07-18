1. 필요한 설치 환경 및 Package
    1). "hosts"에 "<controller_IP>     controller" 추가
        : OpenStack 인증(Get Token) 후 받은 Endpoint 정보를 이용해 각 Service와 연동 할 때
          endpoint의 url 정보가 "controller"로 되어 있는 경우 등록한다.

    2). 설치 파일(use pip)
       a). pip > v8.1 이상
       b). python-neutronclient
       c). python-novaclient
       d). python-keystoneclient
       e). oslo.config
       f). pexpect

2. Configuration
    Test할 network,Subnet,router,VM,SecurityGroup의 Max 수는 config file에서 각각 설정한다.
        예) "network_cnt = 10" 일때 network 설정을 위한 index는 1 ~ 10 사이만 해당된다.
             (network1, network2, ..., network10)