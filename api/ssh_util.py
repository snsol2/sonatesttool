import pexpect
import ast
import socket
from api.instance import InstanceTester
from api.reporter import Reporter
from api.config import ReadConfig

PROMPT = ['~# ', 'onos> ', '\$ ', '\# ', ':~$ ']
CMD_PROMPT = "\[SONA\]\# "

CONFIG_FILE = '../config/config.ini'

class SSHUtil():

    instance = InstanceTester(CONFIG_FILE)
    config = ReadConfig(CONFIG_FILE)

    def __init__(self):
        print '__init__'

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
                print ("[-] Error Connection to SSH Server \n")
                return False
            if ret == 1:
                conn.sendline('yes')
                ret = conn.expect([pexpect.TIMEOUT, '[P|p]assword'], timeout=3)
            if ret == 0:
                print ("[-] Error Connection to SSH Server \n")
                return False

            conn.sendline(password)
            conn.expect(PROMPT, timeout=5)

        except Exception, e:
            print e
            return False

        return conn

    @classmethod
    def ssh_disconnect(cls, ssh_conn):
        ssh_conn.close()

    @classmethod
    def ssh_send_command(cls, ssh_conn, cmd):
        ssh_conn.sendline(cmd)
        ssh_conn.expect(PROMPT)
        return ssh_conn.before

    @classmethod
    def ssh_conn_send_command(cls, conn_info, cmd):
        ssh_conn = cls.ssh_connect(conn_info['host'], conn_info['user'], conn_info['port'], conn_info['password'])
        if ssh_conn is False:
            return False

        ssh_conn.sendline(cmd)
        ssh_conn.expect(PROMPT, timeout=3)
        ssh_conn.close()
        return ssh_conn.before

    @classmethod
    def ssh_ping(cls, inst1, inst2, dest):
        Reporter.unit_test_start()
        ping_ip = dest
        try:
            socket.inet_aton(dest)
        except socket.error:
            ping_ip = cls.instance.get_instance_ip(dest)
            if None is ping_ip:
                Reporter.unit_test_stop('nok')
                return False
            pass

        # instance connection info
        if '' is not inst2:
            name_list = inst2.split(':')

        inst_conf = cls.config.get_instance_config()
        inst_info_1 = ast.literal_eval(inst_conf[inst1])
        if '' is not inst2:
            inst_info_2 = ast.literal_eval(inst_conf[name_list[0]])

        # instance connection info
        # floating ip
        floating_ip = cls.instance.get_instance_floatingip(inst1)
        if None is floating_ip:
            print 'get floating_ip fail : ', floating_ip
            Reporter.unit_test_stop('nok')
            return False

        # print '\n1st ssh_cmd : ', floating_ip, inst_info_1['user'], inst_info_1['password']
        conn = cls.ssh_connect(floating_ip, inst_info_1['user'], '', inst_info_1['password'])
        if conn is False:
            print 'ssh connection failed!!'
            Reporter.unit_test_stop('nok')
            return False

        # instance ip
        if '' is not inst2:
            inst2_ip = cls.instance.get_instance_ip(inst2)
            ssh_cmd = 'ssh ' + inst_info_2['user'] + '@' + inst2_ip
            conn.sendline(ssh_cmd)
            # print '2nd ssh_cmd : ', ssh_cmd
            ssh_newkey = 'Are you sure you want to continue connecting'
            ret = conn.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'], timeout=3)
            if ret == 0:
                print ("[-] Error Connection to SSH Server \n")
                Reporter.unit_test_stop('nok')
                cls.ssh_disconnect(conn)
                return False
            if ret == 1:
                conn.sendline('yes')
                ret = conn.expect([pexpect.TIMEOUT, '[P|p]assword'], timeout=3)
            if ret == 0:
                print ("[-] Error Connection to SSH Server \n")
                Reporter.unit_test_stop('nok')
                cls.ssh_disconnect(conn)
                return False

            conn.sendline(inst_info_2['password'])
            conn.expect(PROMPT, timeout=3)

        cls.change_prompt(conn)

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

        cls.ssh_disconnect(conn)
        if int(result[0]) != 0:
            Reporter.unit_test_stop('nok')
            return False

        Reporter.unit_test_stop('ok')
        return True

    @classmethod
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

    @classmethod
    def onos_apps_status(cls, conn_info):
        switching ='openstackswitching'
        routing = 'openstackrouting'
        networking = 'openstacknetworking'
        node = 'openstacknode'
        interface = 'openstackinterface'

        status = {switching:0, routing:0,
                  networking:0, node:0,
                  interface:0}

        recv_msg = cls.ssh_conn_send_command(conn_info, 'apps -a -s')
        if recv_msg is False:
            # Reporter.unit_test_stop('nok')
            return -1

        # serach
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

        return app_status

    @classmethod
    def onos_device_status(cls, conn_info):
        dev_msg = cls.ssh_conn_send_command(conn_info, 'devices')
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
                # print 'device status ---------- nok'
                return False

            port_status = cls.ssh_conn_send_command(conn_info, 'ports '+dev_list[i]['id'])
            if port_status == False:
                return False

            port_result = cls.onos_port_status(port_status)
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

        # print 'device status ---------- ok'
        if len(dev_list) != br_int_status:
            # print 'port status(br-int) ---------- nok'
            return False

        if len(dev_list) != vxlan_status:
            # print 'port status(vxlan) ---------- nok'
            return False

        return True

    @classmethod
    def onos_port_status(cls, str):
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

    @classmethod
    def onos_devices_status(cls):
        # onos statusa
        Reporter.unit_test_start()
        conn_info = {}
        onos_info = cls.config.get_onos_info()

        for onos_ip in onos_info.onos_list:
            conn_info['host'] = onos_ip
            conn_info['user'] = onos_info.user_id
            conn_info['port'] = onos_info.ssh_port
            conn_info['password'] = onos_info.password
            ret = cls.onos_device_status(conn_info)
            if 'False' is ret:
                Reporter.unit_test_stop('nok')
                break

        Reporter.unit_test_stop('ok')


    @classmethod
    def onos_application_status(cls):
        # onos statusa
        Reporter.unit_test_start()
        conn_info = {}
        onos_info = cls.config.get_onos_info()

        for onos_ip in onos_info.onos_list:
            conn_info['host'] = onos_ip
            conn_info['user'] = onos_info.user_id
            conn_info['port'] = onos_info.ssh_port
            conn_info['password'] = onos_info.password
            ret = cls.onos_apps_status(conn_info)
            if 'False' is ret:
                Reporter.unit_test_stop('nok')
                break

        Reporter.unit_test_stop('ok')
