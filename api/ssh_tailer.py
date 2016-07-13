import pexpect
import threading
from api.reporter import Reporter

PROMPT = ['~# ', '>>> ', 'onos> ', '\$ ', '\# ', ':~$ ', 'onos1:~']

class SSHTailer():
    thr_status_dic = {}
    result_dic = {}

    def __init__(self):
        print '__init__'

    @classmethod
    def ssh_connect(cls, host, user, port, password):
        try:
            ssh_newkey = 'Are you sure you want to continue connecting'
            connStr = 'ssh '+port+user+'@'+host
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
    def ssh_tail_thread(cls, tail_info):
        exit_prompt = False
        # Reporter.PRINTG('%s, %s, %s, %s', tail_info.hostname, tail_info.username, tail_info.password, tail_info.filename)
        ssh_conn = cls.ssh_connect(tail_info.hostname, tail_info.username, '', tail_info.password)
        if ssh_conn is not False:
            ssh_conn.sendline(tail_info.filename)
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
    def ssh_start_tailer(cls, tail_info):
        thr = threading.Thread(target=cls.ssh_tail_thread, args=(tail_info, ))
        cls.thr_status_dic[thr.getName()] = [thr, True]
        cls.result_dic[thr.getName()] = ''
        thr.start()
        print cls.thr_status_dic

    @classmethod
    def ssh_stop_tailer(cls, result, thr_name):
        if 'fail' in result:
            Reporter.REPORT_MSG('%s', cls.result_dic[thr_name])
        if thr_name in cls.result_dic:
            del cls.result_dic[thr_name]
        if cls.thr_status_dic[thr_name][0].getName().find(thr_name) != -1:
            cls.thr_status_dic[thr_name][1] = False
            cls.thr_status_dic[thr_name][0].join(1)

    @classmethod
    def ssh_stop_all_tailer(cls, result):
        for key in cls.thr_status_dic:
            print 'stop_thread_name : ', key
            cls.ssh_stop_tailer(result, key)

        cls.thr_status_dic.clear()
