# Copyright 2016 Telcoware

import logging
import logging.handlers
import datetime
import inspect
from api.config import ReadConfig
import traceback
import sys
import os

WHITE = '\033[1;97m'
BLUE = '\033[1;94m'
YELLOW = '\033[1;93m'
GREEN = '\033[1;92m'
RED = '\033[1;91m'
BLACK = '\033[1;90m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


class Reporter:
    LOG = logging.getLogger(__name__)
    REPORT_LOG = logging.getLogger("report")
    test_count = 0
    ok_count = 0
    nok_count = 0
    skip_count = 0

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
        self.REPORT_LOG.addHandler(file_handler)

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
        print report_format % args,

    @classmethod
    def start_line(cls, call_method):
        test_method = str(cls.test_count) + '. ' + call_method + '... Test'
        cls.NRET_PRINT("%s %s", test_method, ("_" * (70 - len(test_method))))
        cls.REPORT_MSG("\n%s %s", test_method, ("_" * (70 - len(test_method))))
        return

    @classmethod
    def exception_err_write(cls):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        cls.REPORT_MSG("%s", ''.join('   !! ' + line for line in lines))
        cls.unit_test_stop('nok')
        return lines

    @classmethod
    def unit_test_start(cls):
        if cls.test_count == 0:
            cls.REPORT_MSG("\n\n\n    Test Start\n %s", ('='*70))
            print "\nTest Start\n" + ('=' * 80)
        cls.test_count += 1
        method = traceback.extract_stack(None, 2)[0][2]
        # cls.start_line(called_method)
        if method in ['create_instance', 'delete_instance']:
            method = str(cls.test_count) + '. ' + method + ' (wait 5 seconds)'
        else:
            method = str(cls.test_count) + '. ' + method + ' '

        cls.NRET_PRINT("%s %s", method, ("_" * (70 - len(method))))
        cls.REPORT_MSG("\n%s %s", method, ("_" * (70 - len(method))))
        # pass

    @classmethod
    def unit_test_stop(cls, report_string):
        if 'ok' == report_string:
            cls.ok_count += 1
            cls.PRINTG("%s", 'ok')
            # print 'ok test' + report_string % (args[0], args[1], args[2])
        elif 'nok' == report_string:
            cls.nok_count += 1
            cls.PRINTR("%s", 'nok')
            if ReadConfig.get_test_mode() == 'break':
                cls.test_summary()
                os._exit(1)
        elif 'skip' == report_string:
            cls.skip_count += 1
            cls.PRINTB("%s", 'skip')

    @classmethod
    def print_count(cls):
        print cls.test_count

    @classmethod
    def test_summary(cls):
        print "=" * 80
        print "Total: %d (" % cls.test_count,
        print GREEN + "ok:" + ENDC + " %d    " % cls.ok_count,
        print BLUE + "skip:" + ENDC + " %d    " % cls.skip_count,
        print RED + "nok:" + ENDC + " %d )   " % cls.nok_count
