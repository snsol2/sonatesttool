import inspect
from api.reporter import CLog
from api.config import ReadConfig

conf = ReadConfig('../config/config.ini')

c = CLog()


# line_number = inspect.getlineno(inspect.getouterframes(inspect.currentframe()))
# file_name = inspect.getfile(inspect.getouterframes(inspect.currentframe()))

# print line_number, file_name

c.DPRINTG("test")
c.DPRINTDR("test")
