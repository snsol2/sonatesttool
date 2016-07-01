import paramiko
import select
import threading
from api.reporter import Reporter


class SSHTailer:
    strlog = ''
    channel = ''
    tail_thr = ''

    def __init__(self):
        print 'CSSHTailer __init__'

    def __del__(self):
        print 'CSSHTailer __del__'

    @classmethod
    def tail_thread(cls):
        cls.channel.exec_command("tail -f " + cls.file)
        while True:
            if cls.channel.exit_status_ready():
                print 'break'
                break
            rl, wl, xl = select.select([cls.channel], [], [], 0.0)
            if len(rl) > 0:
                cls.strlog += cls.channel.recv(65535)

    @classmethod
    def ssh_start_tailer(self, tail_info):
        # Reporter.PRINTG('%s, %s, %s, %s',
        #                 tail_info.hostname,
        #                 tail_info.username,
        #                 tail_info.password,
        #                 tail_info.filename)
        self.file = tail_info.filename
        self.tail_thr = threading.Thread(target=self.tail_thread)
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname=tail_info.hostname,
                                username=tail_info.username,
                                password=tail_info.password)
        self.channel = self.ssh_client.get_transport().open_session()
        self.tail_thr.start()

    @classmethod
    def ssh_stop_tailer(self, result):
        if result == 'fail':
            Reporter.REPORT_MSG('%s', self.strlog)
        self.strlog=''
        self.tail_thr.join(1)
        self.ssh_client.close()
        return None
