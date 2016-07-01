from pexpect import pxssh

class remote_ssh():
    def __init__(self, config_file):
        self.m_ssh = pxssh.pxssh()

    def __del__(self):
        del self.m_ssh

    def ssh_connect(self, ip, port, user, passwd):
        # self.m_ssh.login(ip, user, password=passwd, port=port, original_prompt='[> ]')
        self.m_ssh.login(ip, user, password=passwd, port=port)

    def ssh_command(self, command):
        self.m_ssh.sendline(command)
        # self.m_ssh.prompt()
        self.m_ssh.set_unique_prompt()
        return self.m_ssh.before

    def ssh_disconnect(self):
        self.m_ssh.logout()
        self.m_ssh.logout()
        self.m_ssh.logout()

