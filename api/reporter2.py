# Copyright 2016 Telcoware

import logging
import logging.handlers
import datetime
import inspect
import pexpect
import threading
import time
import traceback
# from api.config import ReadConfig
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
PROMPT = ['~# ', '>>> ', 'onos> ', '\$ ', '\# ', ':~$ ', 'onos1:~']


class Reporter:
    LOG = logging.getLogger(__name__)
    REPORT_LOG = logging.getLogger("report")

    test_count = 0
    ok_count = 0
    nok_count = 0
    skip_count = 0
    # tailer
    thr_status_dic = {}
    result_dic = {}
    test_mode = ''
    _config = ''

    # def __init__(self, config_file):
    def __init__(self, config):
        # log : console
        log_formatter = logging.Formatter('[%(asctime)s] (%(levelname)7s) %(filename)s:%(lineno)s : %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        self.LOG.addHandler(stream_handler)

        # report : file
        now = datetime.datetime.now()
        now_time = now.strftime('%Y-%m-%d')
        file_name = config.get_file_path() + 'REPORT_' + now_time
        rpt_formatter = logging.Formatter('%(message)s')
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(rpt_formatter)
        self.REPORT_LOG.addHandler(file_handler)

        self.test_mode = config.get_test_mode()
        Reporter._config = config

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

    @classmethod
    def PRINTW(cls, report_format, *args):
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
        cls.start_tailer()

        # if method in ['create_instance', 'delete_instance']:
        #     method = str(cls.test_count) + '. ' + method + ' (wait 5 seconds)'
        # else:
        #     method = str(cls.test_count) + '. ' + method + ' '
        method = str(cls.test_count) + '. ' + method + ' '

        cls.NRET_PRINT("%s %s", method, ("_" * (70 - len(method))))
        cls.REPORT_MSG("\n%s %s", method, ("_" * (70 - len(method))))
        # pass

    @classmethod
    def unit_test_stop(cls, report_string):
        cls.stop_all_tailer(report_string)
        if 'ok' == report_string:
            cls.ok_count += 1
            cls.PRINTG("%s", 'ok')
            # print 'ok test' + report_string % (args[0], args[1], args[2])
        elif 'nok' == report_string:
            cls.nok_count += 1
            cls.PRINTR("%s", 'nok')
            if cls.test_mode == 'break':
                cls.test_summary()
                os._exit(1)
        elif 'skip' == report_string:
            cls.skip_count += 1
            cls.PRINTB("%s", 'skip')

    # @classmethod
    def print_count(cls):
        print cls.test_count

    @classmethod
    def test_summary(cls):
        print "=" * 80
        print "Total: %d (" % cls.test_count,
        print GREEN + "ok:" + ENDC + " %d    " % cls.ok_count,
        print BLUE + "skip:" + ENDC + " %d    " % cls.skip_count,
        print RED + "nok:" + ENDC + " %d )   " % cls.nok_count


#### Tailer Function #####
    @classmethod
    def ssh_connect(cls, port, user, host, password):
        try:
            ssh_newkey = 'Are you sure you want to continue connecting'
            if '' is port:
                connStr = 'ssh '+ user + '@' + host
            else:
                connStr = 'ssh ' + '-p ' + port + ' ' + user + '@' + host
            conn = pexpect.spawn(connStr)
            ret = conn.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'], timeout=1)

            if ret == 0:
                cls.REPORT_MSG('   >> [%s]:tailer Error Connection to SSH Server', host)
                return False
            if ret == 1:
                conn.sendline('yes')
                ret = conn.expect([pexpect.TIMEOUT, '[P|p]assword'], timeout=1)
            if ret == 0:
                cls.REPORT_MSG('   >> [%s]:tailer Error Connection to SSH Server', host)
                return False

            conn.sendline(password)
            conn.expect(PROMPT, timeout=1)
        except Exception, e:
            # print e
            cls.REPORT_MSG('   >> [%s]:tailer Error Connection to SSH Server', host)
            return False

        return conn

    @classmethod
    def tailer_thread(cls, port, user, host, password, file):
        exit_prompt = False
        # Reporter.PRINTG('%s, %s, %s, %s, %s\n', host, user, port, password, file)
        ssh_conn = cls.ssh_connect(port, user, host, password)
        if ssh_conn is not False:
            cls.result_dic[threading.current_thread().getName()] = '[' + host + ', ' + user + ', ' + file + ']\n'
            ssh_conn.sendline('tail -f -n 0 ' + file)
            while cls.thr_status_dic[threading.current_thread().getName()][1]:
                try:
                    # print ('Thread ID : %s' %(threading.current_thread().ident))
                    data = (ssh_conn.read_nonblocking(size=2048, timeout=0.5))
                    cls.result_dic[threading.current_thread().getName()] += data
                    # print data
                    for prompt in PROMPT:
                        if prompt in str(data):
                            exit_prompt = True
                            cls.thr_status_dic[threading.current_thread().getName()][1] = False
                            break
                except Exception, e:
                    if 'Timeout exceeded.' in str(e):
                        pass

            ssh_conn.close()
        else:
            # Error connection to SSH Server
            # print 'Error connection to SSH Server............'
            exit_prompt = True

        cls.REPORT_MSG('   >> Tail_thread[%s] while exit', threading.current_thread().getName())
        if exit_prompt:
            if threading.current_thread().getName() in cls.thr_status_dic:
                del cls.thr_status_dic[threading.current_thread().getName()]


    @classmethod
    def create_start_tailer(cls, port, user, host, password, file):
        thr = threading.Thread(target=cls.tailer_thread, args=(port, user, host, password, file, ))
        cls.thr_status_dic[thr.getName()] = [thr, True]
        cls.result_dic[thr.getName()] = ''
        thr.start()
        # print cls.thr_status_dic

    @classmethod
    def stop_tailer(cls, result, thr_name):
        # Reporter.REPORT_MSG('%s', cls.result_dic[thr_name])
        if 'nok' in result:
            line_list = cls.result_dic[thr_name].splitlines()
            Reporter.REPORT_MSG("%s", '\n'.join('   ** ' + line for line in line_list))
        if thr_name in cls.result_dic:
            del cls.result_dic[thr_name]
        if cls.thr_status_dic[thr_name][0].getName().find(thr_name) != -1:
            cls.thr_status_dic[thr_name][1] = False
            cls.thr_status_dic[thr_name][0].join(1)

    @classmethod
    def stop_all_tailer(cls, result):
        if threading.activeCount() > 1:
            for key in cls.thr_status_dic:
                cls.stop_tailer(result, key)

            cls.thr_status_dic.clear()

    @classmethod
    def start_tailer(cls):
        # onos tail
        onos_info = cls._config.get_onos_info()
        for onos_ip in onos_info.onos_list:
            cls.create_start_tailer('',
                                    onos_info.os_username,
                                    onos_ip,
                                    onos_info.os_password,
                                    onos_info.onos_logfile)
            time.sleep(0.5)

        # openstack tail
        openstack_info = cls._config.get_openstack_info()
        cls.create_start_tailer('',
                                openstack_info.os_username,
                                openstack_info.controller_ip,
                                openstack_info.os_password,
                                openstack_info.log_files)
