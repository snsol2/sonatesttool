import pexpect
import ast
import commands
import socket
import keystoneclient.v2_0.client as kclient
from api.instance import InstanceTester
from api.reporter2 import Reporter
# from api.config import ReadConfig

PROMPT = ['~# ', 'onos> ', '\$ ', '\# ', ':~$ ', '$ ']
CMD_PROMPT = '\[SONA\]\# '


class State:

    def __init__(self, config):
        self.instance = InstanceTester(config)
        self.onos_info = config.get_onos_info()
        self.inst_conf = config.get_instance_config()
        self.auth = config.get_auth_conf()
        self.conn_timeout = config.get_ssh_conn_timeout()
        self.ping_timeout = config.get_floating_ip_check_timeout()

    def ssh_connect(self, host, user, port, password):
        try:
            ssh_newkey = 'want to continue connecting'
            if '' is port:
                connStr = 'ssh ' + user + '@' + host
            else:
                connStr = 'ssh '+ '-p ' + port + ' ' + user + '@' + host
            # Reporter.REPORT_MSG('   >> connection : %s', connStr)
            conn = pexpect.spawn(connStr)
            ret = conn.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'], timeout=self.conn_timeout)
            if ret == 0:
                Reporter.REPORT_MSG('   >> [%s] Error Connection to SSH Servcer(%d)', host, ret)
                return False
            if ret == 1:
                # Reporter.REPORT_MSG('   >> [%s] wait %s ', host, ssh_newkey)
                conn.sendline('yes')
                ret = conn.expect([pexpect.TIMEOUT, '[P|p]assword'], timeout=self.conn_timeout)

            conn.sendline(password)
            conn.expect(PROMPT, timeout=self.conn_timeout)

        except Exception, e:
            Reporter.REPORT_MSG('   >> [%s] Error Connection to SSH Servcer (timeout except)', host)
            return False

        return conn

    def ssh_disconnect(self, ssh_conn):
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

    def ssh_ping(self, inst1, inst2, dest):
        Reporter.unit_test_start()
        try:
            # check dest type
            ping_ip = dest
            try:
                socket.inet_aton(dest)
            except socket.error:
                ping_ip = self.instance.get_instance_ip(dest)
                if None is ping_ip:
                    Reporter.unit_test_stop('nok')
                    return False
                pass

            # floating ip
            floating_ip = self.instance.get_instance_floatingip(inst1)
            if None is floating_ip:
                Reporter.REPORT_MSG('   >> Get floating_ip[%s] fail', floating_ip)
                Reporter.unit_test_stop('nok')
                return False

            # first ssh connection
            # get first instance connection info
            inst_info_1 = ast.literal_eval(self.inst_conf[inst1])
            conn = self.ssh_connect(floating_ip, inst_info_1['user'], '', inst_info_1['password'])
            if conn is False:
                Reporter.unit_test_stop('nok')
                return False

            # get second instance connection info
            if ':' in inst2:
                name_list = inst2.split(':')
                inst_info_2 = ast.literal_eval(self.inst_conf[name_list[0]])
                inst2_ip = self.instance.get_instance_ip(inst2)
                ssh_cmd = 'ssh ' + inst_info_2['user'] + '@' + inst2_ip
                conn.sendline(ssh_cmd)
                # Reporter.REPORT_MSG('   >> connection: %s', ssh_cmd)
                ssh_newkey = 'want to continue connecting'
                ret = conn.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'], timeout=self.conn_timeout)
                if ret == 0:
                    Reporter.REPORT_MSG('   >> [%s] Error Connection to SSH Server(%d)', inst2_ip, ret)
                    Reporter.unit_test_stop('nok')
                    self.ssh_disconnect(conn)
                    return False
                if ret == 1:
                    conn.sendline('yes')
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
                if '' is not inst2:
                    Reporter.REPORT_MSG('   >> result : %s --> %s --> %s : ok',
                                        inst1, inst2, dest)
                else:
                    Reporter.REPORT_MSG('   >> result : %s --> %s : ok',
                                        inst1, dest)
                Reporter.unit_test_stop('ok')
            else:
                if '' is not inst2:
                    Reporter.REPORT_MSG('   >> result : %s --> %s --> %s : nok',
                                        inst1, inst2, dest)
                else:
                    Reporter.REPORT_MSG('   >> result : %s --> %s : nok',
                                        inst1, dest)

                Reporter.REPORT_MSG("%s", '\n'.join('     >> '
                                                    + line for line in ping_list))

                Reporter.unit_test_stop('nok')
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

    def openstack_get_token(self):
        Reporter.unit_test_start()
        try:
            keystone = kclient.Client(auth_url=self.auth['auth_url'],
                                      username=self.auth['username'],
                                      password=self.auth['api_key'],
                                      tenant_name=self.auth['project_id'])
            token = keystone.auth_token
            if not token:
                Reporter.REPORT_MSG("   >> OpentStack Authentication Fail --->")
                Reporter.unit_test_stop('nok')
                return
            Reporter.REPORT_MSG("   >> OpenStack Authentication Succ ---> %s", token)
            Reporter.unit_test_stop('ok')
        except:
            Reporter.exception_err_write()

    def openstack_get_service(self):
        Reporter.unit_test_start()
        try:
            keystone = kclient.Client(auth_url=self.auth['auth_url'],
                                      username=self.auth['username'],
                                      password=self.auth['api_key'],
                                      tenant_name=self.auth['project_id'])
            service_list = [{a.name: a.enabled} for a in keystone.services.list()]

            for i in range(len(service_list)):
                if service_list[i].values()[0] is False:
                    Reporter.REPORT_MSG("   >> OpenStack Service Fail ---> %s", service_list[i])
                    Reporter.unit_test_stop('nok')
                    return

            Reporter.REPORT_MSG("   >> OpenStack Service Succ ---> %s", service_list)
            Reporter.unit_test_stop('ok')

        except:
            Reporter.exception_err_write()

    def floating_ip_check(self, inst1):
        Reporter.unit_test_start()
        try:
            # floating ip
            floating_ip = self.instance.get_instance_floatingip(inst1)
            if None is floating_ip:
                Reporter.REPORT_MSG('   >> Get floating_ip[%s] fail', floating_ip)
                Reporter.unit_test_stop('nok')
                return False
            # floating_ip = '10.10.2.93'
            cmd = 'ping ' + floating_ip + ' -w 1'
            ping_result = []
            sucs_cnt = 0
            for i in range(self.ping_timeout):
                (exitstatus, outtext) = commands.getstatusoutput(cmd)
                # print outtext
                ping_result.append(outtext)
                if 'from ' + floating_ip in outtext:
                    sucs_cnt += 1
                    if 2 is sucs_cnt:
                        break

            if 2 is sucs_cnt:
                Reporter.REPORT_MSG('   >> result : local --> %s : ok', floating_ip)
                Reporter.unit_test_stop('ok')
                return True
            else:
                Reporter.REPORT_MSG('   >> result : local --> %s : nok', floating_ip)
                Reporter.unit_test_stop('nok')
            return False
        except:
            Reporter.exception_err_write()
