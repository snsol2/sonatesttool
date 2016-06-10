1. Test Tool을 동작시키는 System의 "hosts" file에 "controller"가 등록되어 있어야한다.
  - OpenStack 인증(Get Token) 후 Endpoint 정보를 이용해 각 Service와 연동을 하게 되는데
    OpenStack에 등록된 endpoint의 url 정보가 "controller"로 되어 있는 경우 등록한다.