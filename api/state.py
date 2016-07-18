import pexpect
import ast
import socket
import keystoneclient.v2_0.client as kclient
from api.instance import InstanceTester
from api.reporter2 import Reporter
# from api.config import ReadConfig

PROMPT = ['~# ', 'onos> ', '\$ ', '\# ', ':~$ ']
CMD_PROMPT = "\[SONA\]\# "


class State:
    # def __init__(self, config_file):
    def __init__(self, config):
        # self.instance = InstanceTester(config_file)
        # self.onos_info = ReadConfig(config_file).get_onos_info()
        # self.inst_conf = ReadConfig.get_instance_config()
        self.instance = InstanceTester(config)
        self.onos_info = config.get_onos_info()
        self.inst_conf = config.get_instance_config()
        self.auth = config.get_auth_conf()

    @classmethod
    def ssh_connect(cls, host, user, port, password):
        try:
            ssh_newkey = 'Are you sure you want to continue connecting'
            if '' is port:
                connStr = 'ssh ' + user + '@' + host
            else:
                connStr = 'ssh '+ '-p ' + port + ' ' + user + '@' + host
            # print connStr
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
            conn.expect(PROMPT, timeout=5)

        except Exception, e:
            Reporter.REPORT_MSG('   >> [%s] Error Connection to SSH Server', host)
            # print e
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
        ping_ip = dest
        try:
            socket.inet_aton(dest)
        except socket.error:
            ping_ip = self.instance.get_instance_ip(dest)
            if None is ping_ip:
                Reporter.unit_test_stop('nok')
                return False
            pass

        # instance connection info
        if '' is not inst2:
            name_list = inst2.split(':')

        # inst_conf = self.config.get_instance_config()
        inst_info_1 = ast.literal_eval(self.inst_conf[inst1])
        if '' is not inst2:
            inst_info_2 = ast.literal_eval(self.inst_conf[name_list[0]])

        # instance connection info
        # floating ip
        floating_ip = self.instance.get_instance_floatingip(inst1)
        if None is floating_ip:
            Reporter.REPORT_MSG('   >> Get floating_ip[%s] fail', floating_ip)
            Reporter.unit_test_stop('nok')
            return False

        # print '\n1st ssh_cmd : ', floating_ip, inst_info_1['user'], inst_info_1['password']
        conn = self.ssh_connect(floating_ip, inst_info_1['user'], '', inst_info_1['password'])
        if conn is False:
            Reporter.unit_test_stop('nok')
            return False

        # instance ip
        if '' is not inst2:
            inst2_ip = self.instance.get_instance_ip(inst2)
            ssh_cmd = 'ssh ' + inst_info_2['user'] + '@' + inst2_ip
            conn.sendline(ssh_cmd)
            # print '2nd ssh_cmd : ', ssh_cmd
            ssh_newkey = 'Are you sure you want to continue connecting'
            ret = conn.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'], timeout=2)
            if ret == 0:
                Reporter.REPORT_MSG('   >> [%s] Error Connection to SSH Server', inst2_ip)
                Reporter.unit_test_stop('nok')
                self.ssh_disconnect(conn)
                return False
            if ret == 1:
                conn.sendline('yes')
                ret = conn.expect([pexpect.TIMEOUT, '[P|p]assword'], timeout=2)
            if ret == 0:
                Reporter.REPORT_MSG('   >> [%s] Error Connection to SSH Server', inst2_ip)
                Reporter.unit_test_stop('nok')
                self.ssh_disconnect(conn)
                return False

            conn.sendline(inst_info_2['password'])
            conn.expect(PROMPT, timeout=2)

        self.change_prompt(conn)

        cmd = 'ping ' + ping_ip + ' -c 2'
        conn.sendline(cmd)
        conn.expect(CMD_PROMPT)

        # parsing loss rate
        # print '\nret : ' + conn.before
        ping_list = conn.before.splitlines()
        for list in ping_list:
            if 'loss' in list:
                split_list = list.split(', ')
                for x in split_list:
                    if '%' in x:
                        result = x.split('%')
                        break

        self.ssh_disconnect(conn)
        if int(result[0]) != 0:
            Reporter.unit_test_stop('nok')
            return False

        Reporter.unit_test_stop('ok')
        return True

    def change_prompt(self, conn):
        change_cmd = "set prompt='[SONA]\# '"
        for i in range(2):
            try:
                conn.sendline(change_cmd)
                conn.expect(CMD_PROMPT, timeout=1)
                break
            except Exception, e:
                change_cmd = "PS1='[SONA]\# '"
                pass

    def apps_status(self, conn_info):
        switching ='openstackswitching'
        routing = 'openstackrouting'
        networking = 'openstacknetworking'
        node = 'openstacknode'
        interface = 'openstackinterface'

        status = {switching:0, routing:0,
                  networking:0, node:0,
                  interface:0}

        recv_msg = self.ssh_conn_send_command(conn_info, 'apps -a -s')
        if recv_msg is False:
            return 0

        # search
        if recv_msg.find(switching) !=-1:
            status[switching]=1
        if recv_msg.find(routing) !=-1:
            status[routing]=1
        if recv_msg.find(networking) !=-1:
            status[networking]=1
        if recv_msg.find(node) !=-1:
            status[node]=1
        if recv_msg.find(interface) !=-1:
            status[interface]=1

        app_status = (status[switching] & status[routing] &
                      status[networking] & status[node] & status[interface] )

        Reporter.REPORT_MSG('   >> [%s] switch : %d, route : %d, network : %d, node : %d, interface : %d',
                            conn_info['host'], status[switching], status[routing],
                            status[networking], status[node], status[interface] )
        # Reporter.PRINTR('\n switch : %d, route : %d, net : %d, node : %d, inter : %d\n', status[switching], status[routing],
        #               status[networking], status[node], status[interface] )
        return app_status

    def device_status(self, conn_info):
        dev_msg = self.ssh_conn_send_command(conn_info, 'devices')
        if dev_msg is False:
            return False

        #list line split
        dev_list = dev_msg.splitlines()
        dev_list.pop(0) # devices
        dev_list.pop(-1)# onos

        #list to dict
        for i in range(len(dev_list)) :
            str = dev_list[i].replace('Inc.,','')
            cvt_dict = dict(x.split('=') for x in str.split(', '))
            cvt_dict['mfr'] +=', Inc.'
            dev_list[i]=cvt_dict

        result_dic={}

        # avaliable = true check
        br_int_status = 0
        vxlan_status = 0

        for i in range(len(dev_list)):
            if 'false' in dev_list[i]['available']:
                Reporter.REPORT_MSG('   >> device[%s] status nok', dev_list[i]['id'])
                return False

            port_status = self.ssh_conn_send_command(conn_info, 'ports ' + dev_list[i]['id'])
            if port_status == False:
                Reporter.REPORT_MSG('   >> get ssh port %d status error', dev_list[i]['id'])
                return False

            port_result = self.port_status(port_status)
            result_dic[dev_list[i]['id']] = port_result

            # br-int check
            status = 0
            for x in port_result:
                str = dict(x)
                if str.has_key('br-int') == True :
                    status = 1
                    break

            br_int_status += status

            for x in port_result:
                str = dict(x)
                if str.has_key('vxlan') == True:
                    if 'enabled' in str['vxlan']:
                        vxlan_status += 1

        if len(dev_list) != br_int_status:
            Reporter.REPORT_MSG('   >> port status(br-int) -- nok')
            return False

        if len(dev_list) != vxlan_status:
            Reporter.REPORT_MSG('   >> port status(vxlan)  -- nok')
            return False

        Reporter.REPORT_MSG('   >> [%s] device, port status -- ok', conn_info['host'])
        return True

    def port_status(self, str):
        result = [ ]
        port_info_list = str.splitlines()
        del port_info_list[0]
        del port_info_list[0]
        del port_info_list[-1]

        # br-int, vxlan .........proc
        for i in range(len(port_info_list)) :
            port_info_dic = dict(x.split('=') for x in port_info_list[i].split(', '))
            result.append({port_info_dic['portName'] : port_info_dic['state']})

        return result

    # @classmethod
    def onos_devices_status(self):
        # onos status
        Reporter.unit_test_start()
        conn_info = {}
        # onos_info = self.config.get_onos_info()

        for onos_ip in self.onos_info.onos_list:
            conn_info['host'] = onos_ip
            conn_info['user'] = self.onos_info.user_id
            conn_info['port'] = self.onos_info.ssh_port
            conn_info['password'] = self.onos_info.password
            ret = self.device_status(conn_info)
            if False is ret:
                Reporter.unit_test_stop('nok')
                return

        Reporter.unit_test_stop('ok')


    # @classmethod
    def onos_application_status(self):
        # onos status
        Reporter.unit_test_start()
        conn_info = {}
        # onos_info = self.config.get_onos_info()

        for onos_ip in self.onos_info.onos_list:
            conn_info['host'] = onos_ip
            conn_info['user'] = self.onos_info.user_id
            conn_info['port'] = self.onos_info.ssh_port
            conn_info['password'] = self.onos_info.password
            ret = self.apps_status(conn_info)
            if 0 is ret:
                Reporter.unit_test_stop('nok')
                return False

        Reporter.unit_test_stop('ok')

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
