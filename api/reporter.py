# Copyright 2016 Telcoware

import logging
import logging.handlers
import datetime
import inspect
from api.config import ReadConfig

WHITE = '\033[97m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
BLACK = '\033[90m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE ='\033[4m'

class CLog():
    LOG = logging.getLogger(__name__)
    REPORT_LOG = logging.getLogger("report_log")

    def __init__(self, config_file):
        # log : console
        log_fomatter = logging.Formatter('[%(asctime)s] (%(levelname)7s) %(filename)s:%(lineno)s : %(message)s')
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(log_fomatter)
        CLog.LOG.addHandler(streamHandler)

        # report : file
        now = datetime.datetime.now()
        now_time = now.strftime('%Y-%m-%d')
        file_name = ReadConfig(config_file).get_file_path() + 'aaREPORT_' + now_time
        print file_name
        rpt_fomatter = logging.Formatter('%(message)s')
        fileHandler = logging.FileHandler(file_name)
        fileHandler.setFormatter(rpt_fomatter)
        CLog.REPORT_LOG.addHandler(fileHandler)

    @classmethod
    def REPORT_MSG(self, msg, *args):
        full_msg = msg % args
        CLog.REPORT_LOG.error(full_msg)

    @classmethod
    def DPRINTDR(self, format, *args):
        line = inspect.getlineno(inspect.getouterframes(inspect.currentframe())[1][0])
        filename = inspect.getfile(inspect.getouterframes(inspect.currentframe())[1][0])
        fname = filename.split('/')[-1]
        s_time = datetime.datetime.now().time()
        full_msg = '[%s] %s:%d : ' %(s_time, fname, line)
        print RED+full_msg+format % args +ENDC

    @classmethod
    def DPRINTG(self, format, *args):
        line = inspect.getlineno(inspect.getouterframes(inspect.currentframe())[1][0])
        filename = inspect.getfile(inspect.getouterframes(inspect.currentframe())[1][0])
        fname = filename.split('/')[-1]
        s_time = datetime.datetime.now().time()
        full_msg = '[%s] %s:%d : ' %(s_time, fname, line)
        print GREEN+full_msg+format % args +ENDC

    @classmethod
    def DPRINTB(self, format, *args):
        line = inspect.getlineno(inspect.getouterframes(inspect.currentframe())[1][0])
        filename = inspect.getfile(inspect.getouterframes(inspect.currentframe())[1][0])
        fname = filename.split('/')[-1]
        s_time = datetime.datetime.now().time()
        full_msg = '[%s] %s:%d : ' %(s_time, fname, line)
        print BLUE+full_msg+format % args +ENDC

    @classmethod
    def DPRINTY(self, format, *args):
        line = inspect.getlineno(inspect.getouterframes(inspect.currentframe())[1][0])
        filename = inspect.getfile(inspect.getouterframes(inspect.currentframe())[1][0])
        fname = filename.split('/')[-1]
        s_time = datetime.datetime.now().time()
        full_msg = '[%s] %s:%d : ' %(s_time, fname, line)
        print YELLOW+full_msg+format % args +ENDC

    @classmethod
    def DPRINTW(self, format, *args):
        line = inspect.getlineno(inspect.getouterframes(inspect.currentframe())[1][0])
        filename = inspect.getfile(inspect.getouterframes(inspect.currentframe())[1][0])
        fname = filename.split('/')[-1]
        s_time = datetime.datetime.now().time()
        full_msg = '[%s] %s:%d : ' %(s_time, fname, line)
        print WHITE+full_msg+format % args +ENDC

    @classmethod
    def PRINTR(self, format, *args):
        print RED+format % args +ENDC

    @classmethod
    def PRINTG(self, format, *args):
        print GREEN+format % args +ENDC

    @classmethod
    def PRINTB(self, format, *args):
        print BLUE+format % args +ENDC

    @classmethod
    def PRINTY(self, format, *args):
        print YELLOW+format % args +ENDC

    @classmethod
    def PRINTW(self, format, *args):
        print WHITE+format % args +ENDC

    @classmethod
    def NRET_PRINT(self, format, *args):
        print BLUE+format % args +ENDC,

    @classmethod
    def RESULT_PRINT(self, result):
        if result == 'OK':
            CLog.PRINTR('OK')
        elif result == 'NOK' :
            CLog.PRINTR('NOK')
        else :
            CLog.PRINTR('NONE')


