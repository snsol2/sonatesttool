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
BG_WHITE = '\033[0;97m'
BG_BLUEW = '\033[0;37;44m'
BG_SKYW = '\033[0;37;46m'
BG_PINKW = '\033[0;37;45m'
BG_YELLOWW = '\033[0;30;43m'
BG_GREENW = '\033[0;37;42m'
BG_RED = '\033[0;91m'
BG_BLACK = '\033[0;90m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
#PROMPT = ['~# ', '>>> ', 'onos> ', '\$ ', '\# ', ':~$ ', 'onos1:~']
PROMPT = '[#$]'


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
    _config = ''
    test_start_time = datetime.datetime.now()
    test_total_time = datetime.timedelta()
    report_lock = threading.Lock()
    report_file_name =''

    # def __init__(self, config_file):
    def __init__(self, config):
        # log : console
        log_formatter = logging.Formatter('[%(asctime)s] (%(levelname)7s) %(filename)s:%(lineno)s : %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        self.LOG.addHandler(stream_handler)

        # report : file
        now_time=''
        now = datetime.datetime.now()
        format = config.get_report_file_format()
        if 'Day' in format:
            now_time = now.strftime('%Y-%m-%d')
        elif 'Hour' in format:
            now_time = now.strftime('%Y-%m-%d-%H:00')
        elif 'Min' in format:
            now_time = now.strftime('%Y-%m-%d-%H:%M')
        elif 'Sec' in format:
            now_time = now.strftime('%Y-%m-%d-%H:%M:%S')

        file_name = config.get_report_file_path() + 'REPORT_' + now_time
        Reporter.report_file_name = file_name
        rpt_formatter = logging.Formatter('%(message)s')
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(rpt_formatter)
        self.REPORT_LOG.addHandler(file_handler)

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
    def PRINTBL(cls, report_format, *args):
        print BLACK + report_format % args + ENDC

    @classmethod
    def NRET_PRINT(cls, report_format, *args):
        print report_format % args,

    ### Menu Color Func Start ####
    @classmethod
    def PRINTBW(cls, report_format, *args):
        print BG_BLUEW + report_format % args + ENDC

    @classmethod
    def PRINTGW(cls, report_format, *args):
        print BG_GREENW + report_format % args + ENDC

    @classmethod
    def PRINTYW(cls, report_format, *args):
        print BG_YELLOWW + report_format % args + ENDC

    @classmethod
    def PRINTSW(cls, report_format, *args):
        print BG_SKYW + report_format % args + ENDC

    @classmethod
    def PRINTPW(cls, report_format, *args):
        print BG_PINKW + report_format % args + ENDC
    ### Menu Color Func End ####

    @classmethod
    def exception_err_write(cls):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        cls.REPORT_MSG("%s", ''.join('   !! ' + line for line in lines))
        cls.unit_test_stop('nok')
        return lines

    @classmethod
    def exception_err_write2(cls):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        cls.REPORT_MSG("%s", ''.join('   !! ' + line for line in lines))
        return lines

    @classmethod
    def unit_test_start(cls, tail_enable, *args):
        cls.test_start_time = datetime.datetime.now()
        if cls.test_count == 0:
            start_msg = 'Test Start'
            start_time = '(' + cls.test_start_time.strftime('%Y-%m-%d %H:%M:%S') + ')'
            t_msg = start_msg + (' ' * (70 - len(start_msg + start_time))) + start_time
            cls.REPORT_MSG("\n\n\n %s \n %s", t_msg, ('='*70))
            print t_msg + "\n" + ('=' * 80)
        cls.test_count += 1
        method = traceback.extract_stack(None, 2)[0][2]
        method = str(cls.test_count) + '. ' + method + '(' + ', '.join(args) + ')' + ' '
        # method = str(cls.test_count) + '. ' + method

        cls.NRET_PRINT("%s %s", method, ("_" * (70 - len(method))))
        cls.REPORT_MSG("\n%s %s", method, ("_" * (70 - len(method))))
        if True is tail_enable:
            cls.start_tailer()
        # pass

    @classmethod
    def unit_test_stop(cls, report_string, tail_enable=True):
        if True is tail_enable:
            cls.stop_all_tailer(report_string)
        test_duration = datetime.datetime.now() - cls.test_start_time
        cls.test_total_time += test_duration
        cls.REPORT_MSG("\n   >>>%s TEST RESULT: %s (%s)",
                       '-'*20+'>',
                       report_string.upper(),
                       str(test_duration)[:11])

        if 'ok' == report_string:
            cls.ok_count += 1
            cls.PRINTG("%s", 'ok')
        elif 'nok' == report_string:
            cls.nok_count += 1
            cls.PRINTR("%s", 'nok')
            if cls._config.get_test_mode() == 'break':
                cls.test_summary()
                os._exit(1)
        elif 'skip' == report_string:
            cls.skip_count += 1
            cls.PRINTB("%s", 'skip')

    @classmethod
    def test_summary(cls):
        print "=" * 80
        print "Total: %d (" % cls.test_count,
        print GREEN + "ok:" + ENDC + " %d    " % cls.ok_count,
        print BLUE + "skip:" + ENDC + " %d    " % cls.skip_count,
        print RED + "nok:" + ENDC + " %d )    " % cls.nok_count,
        print "   Test Time:",
        print cls.test_total_time

    @classmethod
    def initial_test_count(cls):
        cls.test_count=0
        cls.ok_count=0
        cls.skip_count=0
        cls.nok_count=0
        cls.test_total_time = datetime.timedelta()

#### Tailer Function #####
    @classmethod
    def ssh_connect(cls, port, user, host, password):
        try:
            conn_timeout = cls._config.get_ssh_conn_timeout()
            ssh_newkey = 'want to continue connecting'
            if '' is port:
                connStr = 'ssh '+ user + '@' + host
            else:
                connStr = 'ssh ' + '-p ' + port + ' ' + user + '@' + host

            conn = pexpect.spawn(connStr)
            ret = conn.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:', PROMPT], timeout=conn_timeout)
            if ret == 0:
                cls.REPORT_MSG('   >> [%s] : tailer Error Connection to SSH Server', host)
                cls.ssh_disconnect(conn, host)
                return False
            if ret == 1:
                conn.sendline('yes')
                ret = conn.expect([pexpect.TIMEOUT, '[P|p]assword', PROMPT], timeout=conn_timeout)

            conn.sendline(password)
            conn.expect(PROMPT, timeout=conn_timeout)
        except Exception as e:
            cls.REPORT_MSG('   >> [%s] : tailer Error Connection to SSH Server', host)
            cls.REPORT_MSG('   >>        Error: %s ', e)
            cls.ssh_disconnect(conn, host)
            return False

        return conn

    @classmethod
    def ssh_disconnect(cls, ssh_conn, host):
        try:
            if ssh_conn.isalive():
                ssh_conn.close()
        except Exception as e:
            cls.REPORT_MSG('   >> %s ssh disconnection error(%s)', host, e)


    @classmethod
    def tailer_thread(cls, ssh_conn, host):
        while cls.thr_status_dic[threading.current_thread().getName()][1]:
            try:
                data = (ssh_conn.read_nonblocking(size=2048, timeout=0.05))
                cls.report_lock.acquire()
                cls.result_dic[threading.current_thread().getName()] += data
                cls.report_lock.release()
                # print data
            except Exception, e:
                if 'Timeout exceeded.' in str(e):
                    pass
                else:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                    cls.REPORT_MSG("%s", ''.join('   !! ' + line for line in lines))
        try:
            cls.ssh_disconnect(ssh_conn, host)
        except Exception, e:
            Reporter.REPORT_MSG('   >> [%s] except : %s\n', host, e)

    @classmethod
    def create_start_tailer(cls, port, user, host, password, file, type):
        # Reporter.PRINTG('%s, %s, %s, %s, %s\n', host, user, port, password, file)
        ssh_conn = cls.ssh_connect(port, user, host, password)
        # cls.result_dic[threading.current_thread().getName()] = '[' + host + ', ' + user + ', ' + file + ']\n'
        if ssh_conn is not False:
            # Reporter.REPORT_MSG("%s, join : %s", file, ' '.join(file))
            ssh_conn.sendline('tail -f -n 0 ' + ' '.join(file))
            thr = threading.Thread(target=cls.tailer_thread, args=(ssh_conn, host, ))
            cls.thr_status_dic[thr.getName()] = [thr, True, type, host]
            cls.result_dic[thr.getName()] = ''
            thr.start()

    @classmethod
    def stop_tailer(cls, result, thr_name):
        if 'nok' in result:
            line_list = cls.result_dic[thr_name].splitlines()
            # for i in range(len(line_list)):
            #     if 'tail' in line_list[i]:
            #         del line_list[i]
            #         break;
            Reporter.REPORT_MSG("%s", '\n'.join('     **[' + cls.thr_status_dic[thr_name][2] + ':' + cls.thr_status_dic[thr_name][3] + '] '+ line for line in line_list))
        # if thr_name in cls.result_dic:
        #     del cls.result_dic[thr_name]
        if cls.thr_status_dic[thr_name][0].getName().find(thr_name) != -1:
            cls.thr_status_dic[thr_name][2] = ''
            cls.thr_status_dic[thr_name][1] = False
            cls.thr_status_dic[thr_name][0].join(1)
            if thr_name in cls.result_dic:
                del cls.result_dic[thr_name]

    @classmethod
    def stop_all_tailer(cls, result):
        if threading.activeCount() > 1:
            for key in cls.thr_status_dic:
                cls.stop_tailer(result, key)
            cls.thr_status_dic.clear()

    @classmethod
    def start_tailer(cls):
        # openstack tail
        openstack_info = cls._config.get_openstack_info()
        if True is openstack_info.log_collector:
            cls.create_start_tailer('',
                                    openstack_info.os_username,
                                    openstack_info.controller_ip,
                                    openstack_info.os_password,
                                    openstack_info.log_files, 'openstack')
        # onos tail
        onos_info = cls._config.get_onos_info()
        if True is onos_info.log_collector:
            for onos_ip in onos_info.onos_list:
                cls.create_start_tailer('',
                                        onos_info.os_username,
                                        onos_ip,
                                        onos_info.os_password,
                                        onos_info.onos_logfile, 'onos')

        if openstack_info.log_collector or onos_info.log_collector:
            time.sleep(cls._config.get_log_collector_wait_time())

