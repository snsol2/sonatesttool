import ast
import commands
import os
import socket
import time

import pexpect
from keystoneauth1.identity import v2
from keystoneauth1 import session
from keystoneclient.v2_0 import client

from keystoneclient import exceptions

from api.config import ReadConfig
from api.instance import InstanceTester
from api.network import NetworkTester
from api.onos_info import ONOSInfo
from api.reporter2 import Reporter
from api.identity import Identity

PROMPT = ['~# ', 'onos> ', '\$ ', '\# ', ':~$ ', '$ ']
CMD_PROMPT = '\[SONA\]\# '


class SonaTest:

    def __init__(self, config_file):
        self.conf = ReadConfig(config_file)
        self.onos_info = self.conf.get_onos_info()
        self.inst_conf = self.conf.get_instance_config()
        self.auth = self.conf.get_identity()
        self.conn_timeout = self.conf.get_ssh_conn_timeout()
        self.ping_timeout = self.conf.get_floating_ip_check_timeout()
        self.result_skip_mode = self.conf.get_state_check_result_skip_mode()
        self.wget_url = self.conf.get_wget_url()
        self.instance = InstanceTester(self.conf)
        self.network = NetworkTester(self.conf)
        self.identity = Identity(self.conf)
        self.onos = ONOSInfo(self.conf)
        self.reporter = Reporter(self.conf)

    def ssh_connect(self, host, user, port, password):
        try:
            ssh_newkey = 'want to continue connecting'
            if '' is port:
                connStr = 'ssh ' + user + '@' + host
            else:
                connStr = 'ssh '+ '-p ' + port + ' ' + user + '@' + host
            Reporter.REPORT_MSG('   >> connection : %s', connStr)
            conn = pexpect.spawn(connStr)
            ret = conn.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'], timeout=self.conn_timeout)
            if ret == 0:
                Reporter.REPORT_MSG('   >> [%s] Error Connection to SSH Servcer(%d)', host, ret)
                self.ssh_disconnect(conn)
                return False
            if ret == 1:
                # Reporter.REPORT_MSG('   >> [%s] wait %s ', host, ssh_newkey)
                conn.sendline('yes')
                ret = conn.expect([pexpect.TIMEOUT, '[P|p]assword'], timeout=self.conn_timeout)

            conn.sendline(password)
            conn.expect(PROMPT, timeout=self.conn_timeout)

        except Exception, e:
            Reporter.REPORT_MSG('   >> [%s] Error Connection to SSH Servcer (timeout except)', host)
            self.ssh_disconnect(conn)
            return False

        return conn

    def ssh_disconnect(self, ssh_conn):
        if ssh_conn.isalive():
            ssh_conn.close()

    def ssh_send_command(self, ssh_conn, cmd):
        ssh_conn.sendline(cmd)
        ssh_conn.expect(PROMPT)
        return ssh_conn.before

    def ssh_conn_send_command(self, conn_info, cmd):
        ssh_conn = self.ssh_connect(conn_info['host'], conn_info['user'], conn_info['port'], conn_info['password'])
        if ssh_conn is False:
            return False

        ssh_conn.sendline(cmd)
        ssh_conn.expect(PROMPT, timeout=3)
        ssh_conn.close()
        return ssh_conn.before

    # def ssh_ping(self, inst1, inst2, dest):
    def ssh_ping(self, inst1, *insts):
        if len(insts) > 1:
            Reporter.unit_test_start(False, inst1, insts[0], insts[1])
        else:
            Reporter.unit_test_start(False, inst1, insts[0])

        if len(insts) > 2 or len(insts) < 1:
            Reporter.REPORT_MSG('   >> Check the arguments(Min : 2, Max : 3)')
            Reporter.unit_test_stop('nok', False)
            return False
        try:
            # floating ip
            floating_ip = self.instance.get_instance_floatingip(inst1)
            if None is floating_ip:
                Reporter.REPORT_MSG('   >> Get floating_ip[%s] fail', floating_ip)
                Reporter.unit_test_stop('nok', False)
                return False

            # check dest type
            ping_ip = insts[-1]
            try:
                socket.inet_aton(insts[-1])
            except socket.error:
                ping_ip = self.instance.get_instance_ip(insts[-1])
                if None is ping_ip:
                    Reporter.unit_test_stop('nok', False)
                    return False
                pass

            # clear ssh key
            clear_key = 'ssh-keygen -f "' + os.path.expanduser('~')+'/.ssh/known_hosts" -R ' + floating_ip
            commands.getstatusoutput(clear_key)

            # first ssh connection
            # get first instance connection info
            inst_info_1 = ast.literal_eval(self.inst_conf[inst1])
            conn = self.ssh_connect(floating_ip, inst_info_1['user'], '', inst_info_1['password'])
            if conn is False:
                Reporter.unit_test_stop('nok', False)
                return False

            # get second instance connection info
            if len(insts) > 1:
            # if ':' in inst2:
                name_list = insts[0].split(':')
                inst_info_2 = ast.literal_eval(self.inst_conf[name_list[0]])
                inst2_ip = self.instance.get_instance_ip(insts[0])
                ssh_cmd = 'ssh ' + inst_info_2['user'] + '@' + inst2_ip
                conn.sendline(ssh_cmd)
                # Reporter.REPORT_MSG('   >> connection: %s', ssh_cmd)
                ssh_newkey = 'want to continue connecting'
                ret = conn.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'], timeout=self.conn_timeout)
                if ret == 0:
                    Reporter.REPORT_MSG('   >> [%s] Error Connection to SSH Server(%d)', inst2_ip, ret)
                    Reporter.unit_test_stop('nok', False)
                    self.ssh_disconnect(conn)
                    return False
                if ret == 1:
                    conn.sendline('yes')
                    ret = conn.expect([pexpect.TIMEOUT, '[P|p]assword'], timeout=self.conn_timeout)
                if ret == 2:
                    ret = conn.expect([pexpect.TIMEOUT, '[P|p]assword'], timeout=self.conn_timeout)

                conn.sendline(inst_info_2['password'])
                conn.expect(PROMPT, timeout=self.conn_timeout)

            cmd = 'ping ' + ping_ip + ' -w 2'
            conn.sendline(cmd)
            conn.expect(PROMPT, timeout=self.conn_timeout)

            # parsing loss rate
            ping_list = conn.before.splitlines()
            self.ssh_disconnect(conn)
            ping_result = False
            for list in ping_list:
                if 'loss' in list:
                    split_list = list.split(', ')
                    for x in split_list:
                        if '%' in x:
                            result = x.split('%')
                            if 0 is int(result[0]):
                                ping_result = True
                            break

            # result output
            if True is ping_result:
                if len(insts) > 1:
                    Reporter.REPORT_MSG('   >> result : %s --> %s --> %s : ok',
                                        inst1, insts[0], insts[-1])
                else:
                    Reporter.REPORT_MSG('   >> result : %s --> %s : ok',
                                        inst1, insts[-1])
                Reporter.unit_test_stop('ok', False)
            else:
                if len(insts) > 1:
                    Reporter.REPORT_MSG('   >> result : %s --> %s --> %s : nok',
                                        inst1, insts[0], insts[-1])
                else:
                    Reporter.REPORT_MSG('   >> result : %s --> %s : nok',
                                        inst1, insts[-1])

                Reporter.REPORT_MSG("%s", '\n'.join('     >> '
                                                    + line for line in ping_list))

                Reporter.unit_test_stop('nok', False)
                return False

            return True
        except:
            Reporter.exception_err_write()
            return False

    def change_prompt(self, conn):
        change_cmd = "set prompt='[SONA]\# '"
        for i in range(2):
            try:
                # print change_cmd
                conn.sendline(change_cmd)
                conn.expect(CMD_PROMPT, timeout=1)
                # print '===== set comp'
                break
            except Exception, e:
                change_cmd = "PS1='[SONA]\# '"
                pass

    def openstack_get_token(self, report_flag=None):
        if report_flag is None:
            Reporter.unit_test_start(True)

        try:
            auth = v2.Password(username=self.auth['username'],
                               password=self.auth['password'],
                               tenant_name=self.auth['tenant_id'],
                               auth_url=self.auth['auth_url'])
            sess = session.Session(auth=auth, timeout=5)

            token = sess.get_token()
            if not token:
                Reporter.REPORT_MSG("   >> OpentStack Authentication NOK ---> get token fail")
                if report_flag is None:
                    Reporter.unit_test_stop('nok')
                return False
            else:
                Reporter.REPORT_MSG("   >> OpenStack Authentication OK ---> user: %s, token: %s",
                                    self.auth['username'], token)

            if report_flag is None:
                Reporter.unit_test_stop('ok')
            return True

        except exceptions.AuthorizationFailure, err:
            Reporter.REPORT_MSG("   >> OpentStack Authentication Fail ---> %s", err)
            return False
        except exceptions.Unauthorized, err:
            Reporter.REPORT_MSG("   >> OpentStack Authentication Fail ---> %s", err)
            return False
        except:
            # if report_flag is None:
            Reporter.exception_err_write()
            return False

    def openstack_get_service(self, report_flag=None):
        if report_flag is None:
            Reporter.unit_test_start(True)
        try:
            auth = v2.Password(username=self.auth['username'],
                               password=self.auth['password'],
                               tenant_name=self.auth['tenant_id'],
                               auth_url=self.auth['auth_url'])
            sess = session.Session(auth=auth, timeout=5)
            keystone = client.Client(session=sess)

            service_list = [{a.name: a.enabled} for a in keystone.services.list()]

            for i in range(len(service_list)):
                if service_list[i].values()[0] is False:
                    Reporter.REPORT_MSG("   >> OpenStack Service status NOK ---> %s", service_list[i])
                    if report_flag is None:
                        Reporter.unit_test_stop('nok')
                    return False

            Reporter.REPORT_MSG("   >> OpenStack Service status OK ---> %s", service_list)

            if report_flag is None:
                Reporter.unit_test_stop('ok')

            return True

        except exceptions.AuthorizationFailure, err:
            Reporter.REPORT_MSG("   >> OpentStack Authentication Fail ---> %s", err)
            return False
        except exceptions.Unauthorized, err:
            Reporter.REPORT_MSG("   >> OpentStack Authentication Fail ---> %s", err)
            return False
        except:
            # if report_flag is None:
            Reporter.exception_err_write()

    def floating_ip_check(self, inst1):
        Reporter.unit_test_start(False)
        try:
            # floating ip
            floating_ip = self.instance.get_instance_floatingip(inst1)
            if None is floating_ip:
                Reporter.REPORT_MSG('   >> Get floating_ip[%s] fail', floating_ip)
                Reporter.unit_test_stop('nok', False)
                return False
            ping_result = []
            sucs_cnt = 0
            (exitstatus, outtext) = commands.getstatusoutput('uname -a')
            if 'Linux' in outtext:
                cmd = 'ping ' + floating_ip + ' -w 1'
            else:
                cmd = 'ping -t 1 ' + floating_ip

            for i in range(self.ping_timeout):
                (exitstatus, outtext) = commands.getstatusoutput(cmd)
                ping_result.append(outtext)
                if 'from ' + floating_ip in outtext:
                    sucs_cnt += 1
                    if 2 is sucs_cnt:
                        break

            if 2 is sucs_cnt:
                Reporter.REPORT_MSG('   >> result : local --> %s : ok', floating_ip)
                time.sleep(5)
                Reporter.unit_test_stop('ok', False)
                return True
            else:
                Reporter.REPORT_MSG('   >> result : local --> %s : nok', floating_ip)
                Reporter.unit_test_stop('nok', False)
            return False
        except:
            Reporter.exception_err_write()

    def onos_and_openstack_check(self):
        Reporter.unit_test_start(True)
        try:
            flag = 'no'

            app_stat = self.onos.application_status(report_flag=flag)
            device_stat = self.onos.devices_status(report_flag=flag)
            token_stat = self.openstack_get_token(report_flag=flag)
            service_stat = self.openstack_get_service(report_flag=flag)

            # Reporter.NRET_PRINT("%s %s %s %s", app_stat, device_stat, token_stat, service_stat)
            if (app_stat and device_stat and token_stat and service_stat):
                Reporter.unit_test_stop('ok')
            else:
                Reporter.unit_test_stop('nok')
                if False is self.result_skip_mode:
                    Reporter.test_summary()
                    os._exit(1)
        except:
            Reporter.exception_err_write()


    # def ssh_wget(self, inst1, [inst2]):
    def ssh_wget(self, *insts):
        try:
            if len(insts) in [1, 2]:
                Reporter.unit_test_start(False, *insts)

                floating_ip = self.instance.get_instance_floatingip(insts[0])
                if None is floating_ip:
                    Reporter.REPORT_MSG('   >> Get floating_ip[%s] fail', floating_ip)
                    Reporter.unit_test_stop('nok', False)
                    return False

                clear_key = 'ssh-keygen -f "' + os.path.expanduser('~')+'/.ssh/known_hosts" -R ' + floating_ip
                commands.getstatusoutput(clear_key)
            else:
                Reporter.unit_test_start(False, *insts)
                Reporter.REPORT_MSG('   >> Check the arguments(need 1 or 2)')
                Reporter.unit_test_stop('nok', False)
                return False

            cmd = 'wget ' + self.wget_url
            Reporter.REPORT_MSG('   >> wget %s', self.wget_url)
            wget_result = self.wget_ssh_cmd(cmd, *insts)
            if wget_result[0] is True or wget_result[0] is 'timeoutError':
                if self.wget_progress_check(wget_result[1]):
                    self.wget_clear(*insts)
                    Reporter.unit_test_stop('ok')
                    return True
            if wget_result[0] is 'sshConFail':
                return False
            elif wget_result[0] is 'unexpectedError' or wget_result[0] is 'timeoutError':
                Reporter.REPORT_MSG('   >>    Interface MTU size DOWN to 1400')
                cmd = 'sudo ifconfig eth0 mtu 1400;'
                if self.wget_ssh_cmd(cmd, *insts)[0] is False:
                    Reporter.REPORT_MSG('   >> Interface mtu size down fail')
                    Reporter.unit_test_stop('nok', False)
                    return False

                Reporter.REPORT_MSG('   >> second wget %s', self.wget_url)
                cmd = 'wget ' + self.wget_url
                wget_sd_result = self.wget_ssh_cmd(cmd, *insts)
                if wget_sd_result[0] is True or wget_sd_result[0] is 'timeoutError':
                    if self.wget_progress_check(wget_sd_result[1]) is True:
                        Reporter.REPORT_MSG('   >>    Please check MTU SIZE on ALL DATA PATH ~ !!!')
                        Reporter.REPORT_MSG('   >>    You should be set more 1600 bytes for Data Path interfaces  !!!')
                    else:
                        Reporter.REPORT_MSG('   >>  Second wget fail ~ !!!')
                        Reporter.unit_test_stop('nok', False)
                        return False
                    self.wget_clear(*insts)
                else:
                    Reporter.unit_test_stop('nok', False)
                    return False

                Reporter.REPORT_MSG('   >>    Interface MTU size RETURN to 1500')
                cmd = 'sudo ifconfig eth0 mtu 1500'
                if self.wget_ssh_cmd(cmd, *insts)[0] is False:
                    Reporter.REPORT_MSG('   >> Interface mtu size return fail')
                    Reporter.unit_test_stop('nok', False)
                    return False

                Reporter.unit_test_stop('nok', False)

        except:
            Reporter.exception_err_write()
        return True

    def wget_progress_check(self, wget_lines):
        wget_percent = ''
        wget_progress = ''
        for line in wget_lines:
            if 'error' in line.lower():
                Reporter.REPORT_MSG('   >> wget request fail: "%s"', line)
                return False
            elif '%' in line:
                wget_percent = line.split('%')[0].split(' ')[-1]
                wget_progress = line

        if not wget_progress is '':
            if int(wget_percent) in range(1, 101):
                Reporter.REPORT_MSG('   >> wet download Succ : \n   >>     "%s"', wget_progress)
                return True
            else:
                Reporter.REPORT_MSG('   >> wet download low : \n   >>     "%s"', wget_progress)
            return False
        else:
            return False


    def wget_clear(self, *insts):
        Reporter.REPORT_MSG('   >> all wget process kill / download file and all wget log files delete.')
        cmd = 'killall -9 wget; ' + 'rm ' + self.wget_url.split('/')[-1] + '*' + ' ' + 'wget-log*'
        self.wget_ssh_cmd(cmd, *insts)

        return

    def wget_ssh_cmd(self, cmd, *insts):
        # floating ip
        floating_ip = self.instance.get_instance_floatingip(insts[0])
        if None is floating_ip:
            Reporter.REPORT_MSG('   >> Get floating_ip[%s] fail', floating_ip)
            Reporter.unit_test_stop('nok', False)
            return ['sshConFail']

        inst_info_1 = ast.literal_eval(self.inst_conf[insts[0]])
        sudo_key = 'password for ' + inst_info_1['user']
        conn = self.ssh_connect(floating_ip, inst_info_1['user'], '', inst_info_1['password'])
        if conn is False:
            Reporter.REPORT_MSG('   >>  %s ssh connection fail.', insts[0])
            Reporter.unit_test_stop('nok', False)
            return ['sshConFail']

        # get second instance connection info
        if len(insts) is 2:
            name_list = insts[1].split(':')
            inst_info_2 = ast.literal_eval(self.inst_conf[name_list[0]])
            inst2_ip = self.instance.get_instance_ip(insts[1])
            ssh_cmd = 'ssh ' + inst_info_2['user'] + '@' + inst2_ip
            sudo_key = 'password for ' + inst_info_2['user']
            Reporter.REPORT_MSG('   >> second instance SSH connecting(%s)', inst2_ip)
            conn.sendline(ssh_cmd)

            ssh_newkey = 'want to continue connecting'
            ret = conn.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'], timeout=2)
            if ret == 0:
                Reporter.REPORT_MSG('   >> [%s] Error Connection to SSH Server(%d)', inst2_ip, ret)
                Reporter.unit_test_stop('nok', False)
                self.ssh_disconnect(conn)
                return ['sshConFail']
            if ret == 1:
                conn.sendline('yes')
                conn.expect([pexpect.TIMEOUT, '[P|p]assword'], timeout=self.conn_timeout)
            if ret == 2:
                conn.expect([pexpect.TIMEOUT, '[P|p]assword'], timeout=self.conn_timeout)

            conn.sendline(inst_info_2['password'])
            conn.expect(PROMPT, timeout=self.conn_timeout)

        try:
            if 'sudo' not in cmd:
                conn.sendline(cmd)
                conn.expect(PROMPT, timeout=self.conn_timeout)
            elif 'sudo' in cmd:
                conn.sendline(cmd)
                ret = conn.expect([pexpect.TIMEOUT, sudo_key, '[P|p]assword'], timeout=self.conn_timeout)
                if ret == 2:
                    conn.expect([pexpect.TIMEOUT, '[P|p]assword'], timeout=self.conn_timeout)
                conn.sendline(inst_info_1['password'])
                conn.expect(PROMPT, timeout=self.conn_timeout)
        except pexpect.TIMEOUT:
            Reporter.REPORT_MSG('   >> wget download Timeout. limit %s second', self.conn_timeout)
            # self.wget_clear(*insts)
            self.ssh_disconnect(conn)
            return ['timeoutError', conn.before.splitlines()]
        except:
            Reporter.REPORT_MSG('   >> Unexpected Error.')
            return ['unexpectedError', conn.before.splitlines()]

        self.ssh_disconnect(conn)
        return [True, conn.before.splitlines()]


