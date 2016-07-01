import inspect
from api.reporter import Reporter
from api.config import ReadConfig

conf = ReadConfig('../config/config.ini')

c = Reporter()


c.DPRINTG("test")
c.DPRINTDR("test")


