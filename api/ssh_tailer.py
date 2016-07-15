import pexpect
import threading
import time
# from api.reporter import Reporter
from api.config import ReadConfig

PROMPT = ['~# ', '>>> ', 'onos> ', '\$ ', '\# ', ':~$ ', 'onos1:~']
CONFIG_FILE = '../config/config.ini'

class tailer():
    thr_status_dic = {}
    result_dic = {}

    def __init__(self):
        self.onos_info = ReadConfig.get_onos_info()
        self.openstack_info = ReadConfig.get_openstack_info()
        pass

    def ssh_connect(self, port, user, host, password):
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
                Reporter.REPORT_MSG('   >> [%s] Error Connection to SSH Server', host)
                return False
            if ret == 1:
                conn.sendline('yes')
                ret = conn.expect([pexpect.TIMEOUT, '[P|p]assword'], timeout=3)
            if ret == 0:
                Reporter.REPORT_MSG('   >> [%s] Error Connection to SSH Server', host)
                return False

            conn.sendline(password)
            conn.expect(PROMPT, timeout=3)
        except Exception, e:
            # print e
            Reporter.REPORT_MSG('   >> [%s] Error Connection to SSH Server', host)
            return False

        return conn

    def tailer_thread(self, port, user, host, password, file):
        exit_prompt = False
        # Reporter.PRINTG('%s, %s, %s, %s, %s\n', host, user, port, password, file)
        ssh_conn = self.ssh_connect(port, user, host, password)
        if ssh_conn is not False:
            self.result_dic[threading.current_thread().getName()] = '[' + host + ', ' + user + ', ' + file + ']\n'
            ssh_conn.sendline('tail -f -n 0 ' + file)
            while self.thr_status_dic[threading.current_thread().getName()][1]:
                try:
                    # print ('Thread ID : %s' %(threading.current_thread().ident))
                    data = (ssh_conn.read_nonblocking(size=2048, timeout=0.5))
                    self.result_dic[threading.current_thread().getName()] += data
                    print data
                    for prompt in PROMPT:
                        if prompt in str(data):
                            exit_prompt = True
                            self.thr_status_dic[threading.current_thread().getName()][1] = False
                            break
                except Exception, e:
                    if 'Timeout exceeded.' in str(e):
                        pass

            ssh_conn.close()
        else:
            # Error connection to SSH Server
            exit_prompt = True

        Reporter.REPORT_MSG('   >> Tail_thread[%s] while exit', threading.current_thread().getName())
        if exit_prompt:
            if threading.current_thread().getName() in self.thr_status_dic:
                del self.thr_status_dic[threading.current_thread().getName()]


    def create_start_tailer(self, port, user, host, password, file):
        thr = threading.Thread(target=self.tailer_thread, args=(port, user, host, password, file, ))
        self.thr_status_dic[thr.getName()] = [thr, True]
        self.result_dic[thr.getName()] = ''
        thr.start()
        # print self.thr_status_dic

    def stop_tailer(self, result, thr_name):
        if 'nok' in result:
            # Reporter.REPORT_MSG('%s', self.result_dic[thr_name])
            line_list = self.result_dic[thr_name].splitlines()
            Reporter.REPORT_MSG("%s", '\n'.join('   ** ' + line for line in line_list))
        if thr_name in self.result_dic:
            del self.result_dic[thr_name]
        if self.thr_status_dic[thr_name][0].getName().find(thr_name) != -1:
            self.thr_status_dic[thr_name][1] = False
            self.thr_status_dic[thr_name][0].join(1)

    def stop_all_tailer(self, result):
        for key in self.thr_status_dic:
            self.stop_tailer(result, key)

        self.thr_status_dic.clear()

    def start_tailer(self):
        # onos tail
        for onos_ip in self.onos_info.onos_list:
            self.create_start_tailer('', self.onos_info.os_username,
                             onos_ip, self.onos_info.os_password,
                             self.onos_info.onos_logfile)
            time.sleep(0.5)

        # openstack tail
        self.create_start_tailer('', self.openstack_info.username,
                         self.openstack_info.hostname,
                         self.openstack_info.password,
                         self.openstack_info.filename)
