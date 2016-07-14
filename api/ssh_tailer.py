import pexpect
import threading
import time
from api.reporter import Reporter
from api.config import ReadConfig

PROMPT = ['~# ', '>>> ', 'onos> ', '\$ ', '\# ', ':~$ ', 'onos1:~']
CONFIG_FILE = '../config/config.ini'

class SSHTailer():
    thr_status_dic = {}
    result_dic = {}
    config = ReadConfig(CONFIG_FILE)

    def __init__(self):
        print '__init__'

    @classmethod
    def ssh_connect(cls, port, user, host, password):
        try:
            ssh_newkey = 'Are you sure you want to continue connecting'
            if '' is port:
                connStr = 'ssh '+ user + '@' + host
            else:
                connStr = 'ssh ' + '-p ' + port + ' ' + user + '@' + host
            print connStr
            conn = pexpect.spawn(connStr)
            ret = conn.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'], timeout=3)

            if ret == 0:
                print ("[-] Error Connection to SSH Server \n")
                return False
            if ret == 1:
                conn.sendline('yes')
                ret = conn.expect([pexpect.TIMEOUT, '[P|p]assword'], timeout=3)
            if ret == 0:
                print ("[-] Error Connection to SSH Server \n")
                return False

            conn.sendline(password)
            conn.expect(PROMPT, timeout=3)
        except Exception, e:
            print e
            return False

        return conn

    @classmethod
    def ssh_tail_thread(cls, port, user, host, password, file):
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
                    print data
                    for prompt in PROMPT:
                        if prompt in str(data):
                            print 'prompt.....exit'
                            exit_prompt = True
                            cls.thr_status_dic[threading.current_thread().getName()][1] = False
                            break
                except Exception, e:
                    if 'Timeout exceeded.' in str(e):
                        pass

            ssh_conn.close()
        else:
            # Error connection to SSH Server
            exit_prompt = True

        if exit_prompt:
            if threading.current_thread().getName() in cls.thr_status_dic:
                del cls.thr_status_dic[threading.current_thread().getName()]

        print 'tail_thread while exit'

    @classmethod
    def start_tailer(cls, port, user, host, password, file):
        thr = threading.Thread(target=cls.ssh_tail_thread, args=(port, user, host, password, file, ))
        cls.thr_status_dic[thr.getName()] = [thr, True]
        cls.result_dic[thr.getName()] = ''
        thr.start()
        # print cls.thr_status_dic

    @classmethod
    def ssh_stop_tailer(cls, result, thr_name):
        if 'nok' in result:
            # Reporter.REPORT_MSG('%s', cls.result_dic[thr_name])
            line_list = cls.result_dic[thr_name].splitlines()
            Reporter.REPORT_MSG("%s", '\n'.join('   ** ' + line for line in line_list))
        if thr_name in cls.result_dic:
            del cls.result_dic[thr_name]
        if cls.thr_status_dic[thr_name][0].getName().find(thr_name) != -1:
            cls.thr_status_dic[thr_name][1] = False
            cls.thr_status_dic[thr_name][0].join(1)

    @classmethod
    def ssh_stop_all_tailer(cls, result):
        for key in cls.thr_status_dic:
            # print 'stop_thread_name : ', key
            cls.ssh_stop_tailer(result, key)

        cls.thr_status_dic.clear()

    @classmethod
    def ssh_start_tailer(cls):
        # onos tail
        onos_info = cls.config.get_onos_info()
        for onos_ip in onos_info.onos_list:
            cls.start_tailer('', onos_info.os_username,
                             onos_ip, onos_info.os_password,
                             onos_info.onos_logfile)
            time.sleep(0.5)

        # openstack tail
        openstack_info = cls.config.get_openstack_info()
        cls.start_tailer('', openstack_info.username,
                         openstack_info.hostname,
                         openstack_info.password,
                         openstack_info.filename)
