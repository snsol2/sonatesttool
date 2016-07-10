import inspect
from keystoneauth1.identity import v2
from keystoneauth1 import session
from api.reporter import Reporter
from api.config import ReadConfig

conf = ReadConfig('../config/config.ini')

c = Reporter()


# c.DPRINTG("test")
# c.DPRINTDR("test")

net_auth = conf.get_net_auth_conf()
token = v2.Password
print net_auth


