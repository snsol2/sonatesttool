# Copyright 2016 Telcoware

import logging
import logging.handlers
import datetime
import inspect
from api.config import ReadConfig
import traceback
import sys
import os

WHITE = '\033[97m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
BLACK = '\033[90m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


class Reporter:
    LOG = logging.getLogger(__name__)
    REPORT_LOG = logging.getLogger("report")

    def __init__(self):
        # log : console
        log_formatter = logging.Formatter('[%(asctime)s] (%(levelname)7s) %(filename)s:%(lineno)s : %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        self.LOG.addHandler(stream_handler)

        # report : file
        now = datetime.datetime.now()
        now_time = now.strftime('%Y-%m-%d')
        file_name = ReadConfig.get_file_path() + 'REPORT_' + now_time
        # print file_name
        rpt_formatter = logging.Formatter('%(message)s')
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(rpt_formatter)
        Reporter.REPORT_LOG.addHandler(file_handler)

        # report result
        test_count = 0

    @classmethod
    def make_line_header(cls):
        now_time = datetime.datetime.now().time()
        line_number = inspect.getlineno(inspect.getouterframes(inspect.currentframe())[2][0])
        file_path_name = inspect.getfile(inspect.getouterframes(inspect.currentframe())[2][0])
        file_name = file_path_name.split('/')[-1]
        line_header = '[%s] %s:%d : ' % (now_time, file_name, line_number)
        return line_header


    @classmethod
    def REPORT_MSG(cls, report_msg, *args):
        report_msg = report_msg % args
        cls.REPORT_LOG.error(report_msg)

    @classmethod
    def DPRINTDR(cls, report_format, *args):
        line_header = cls.make_line_header()
        print RED + line_header + report_format % args + ENDC

    @classmethod
    def DPRINTG(cls, report_format, *args):
        line_header = cls.make_line_header()
        print GREEN + line_header + report_format % args + ENDC

    @classmethod
    def DPRINTB(cls, report_format, *args):
        line_header = cls.make_line_header()
        print BLUE + line_header + report_format % args + ENDC

    @classmethod
    def DPRINTY(cls, report_format, *args):
        line_header = cls.make_line_header()
        print YELLOW + line_header + report_format % args + ENDC

    @classmethod
    def DPRINTW(cls, report_format, *args):
        line_header = cls.make_line_header()
        print WHITE + line_header + report_format % args + ENDC

    @classmethod
    def PRINTR(cls, report_format, *args):
        print RED + report_format % args + ENDC

    @classmethod
    def PRINTG(cls, report_format, *args):
        print GREEN + report_format % args + ENDC

    @classmethod
    def PRINTB(cls, report_format, *args):
        print BLUE + report_format % args + ENDC

    @classmethod
    def PRINTY(cls, report_format, *args):
        print YELLOW + report_format % args + ENDC

    def PRINTW(self, report_format, *args):
        print WHITE + report_format % args + ENDC

    @classmethod
    def NRET_PRINT(cls, report_format, *args):
        print BLUE + report_format % args + ENDC,

    @classmethod
    def RESULT_PRINT(cls, result):
        if result == 'OK':
            cls.PRINTR('OK')
        elif result == 'NOK' :
            cls.PRINTR('NOK')
        else :
            cls.PRINTR('NONE')

    @classmethod
    def base_line(cls, text):
        print_line = text + ' ' + "=" * (80 - len(text))
        cls.PRINTY(print_line)
        return


    # @classmethod
    # def test(cls, report_string, *args):
    #     if 'ok' in args:
    #         print 'ok test' + report_string % args
    #         # print 'ok test' + report_string % (args[0], args[1], args[2])
    #     elif 'nok' in args:
    #         print 'nok test' + report_string % args

    @classmethod
    def exception_err_write(cls):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)
        return lines

    @classmethod
    def unit_test_start(cls):
        called_method = traceback.extract_stack(None, 2)[0][2]
        cls.base_line(called_method)
        # pass


