from pexpect import pxssh


class RemoteSSH:
    def __init__(self, config_file):
        self.m_ssh = pxssh.pxssh()

    def __del__(self):
        del self.m_ssh

    def ssh_connect(self, ip, user, passwd):
        self.m_ssh.login(ip, user, passwd)

    def ssh_command(self, command):
        self.m_ssh.sendline(command)
        self.m_ssh.prompt()
        return self.m_ssh.before

    def ssh_disconnect(self):
        self.m_ssh.logout()
        self.m_ssh.logout()

