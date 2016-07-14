import pexpect
import datetime
from api.reporter import Reporter

PROMPT = ['~# ', 'onos> ', '\$ ', '\# ', ':~$ ', '\% ']
# PROMPT = '[#$%] '
CMD_PROMPT = "\[SONA\]\# "
# CMD_PROMPT = "[SONA::Prompt] "
# CMD_PROMPT = "[SONA]\$ "

class SSHUtil():

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
            conn.expect(PROMPT, timeout=5)
            # print conn.before
            # cls.change_prompt(conn)

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
        # print ssh_conn.before
        return ssh_conn.before

    @classmethod
    def ssh_conn_send_command(cls, conn_info, cmd):
        Reporter.PRINTR('%s, %s, %s, %s', conn_info.hostname, conn_info.username, conn_info.password, cmd)
        # Reporter.PRINTR('%s, %s, %s, %s, %s', conn_info.hostname, conn_info.username, conn_info.password, conn_info.port, cmd)
        if 'port' in conn_info:
            port = '-p ' + conn_info.port + ' '
        else:
            port = ''

        ssh_conn = cls.ssh_connect(conn_info.hostname, conn_info.username, port, conn_info.password)
        if ssh_conn is False:
            return False

        # print '====================11'
        ssh_conn.sendline(cmd)
        ssh_conn.expect(CMD_PROMPT, timeout=3)
        ssh_conn.close()
        # print ssh_conn.before
        # print '----------------------------222'
        return ssh_conn.before

    @classmethod
    def onos_application_status(cls, conn_info):
        switching ='openstackswitching'
        routing = 'openstackrouting'
        networking = 'openstacknetworking'
        node = 'openstacknode'
        interface = 'openstackinterface'

        status = {switching:0, routing:0,
                  networking:0, node:0,
                  interface:0}

        recv_msg = cls.ssh_conn_send_command(conn_info, 'apps -a -s')
        # Reporter.PRINTR("recv : %s", recv_msg)
        if recv_msg is False:
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

        if app_status == 1:
            print 'application status ------ ok'
        else:
            print 'application status ------ nok'

        # Reporter.PRINTG("open switching : %d, routing : %d, networking : %d, node : %d, interface : %d",
        #                 status[switching], status[routing],
        #                 status[networking], status[node],
        #                 status[interface])

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

        # port_list = ['\x1b[0mports of:cafe000000000031\n'
        # 'id=of:cafe000000000031, available=true, role=MASTER, type=SWITCH, mfr=Nicira, Inc., hw=Open vSwitch, sw=2.3.2, serial=None, managementAddress=10.10.2.31, protocol=OF_13, channelId=10.10.2.31:53397\n'
        # '  port=local, state=disabled, type=copper, speed=0 , portName=br-int, portMac=08:00:27:7b:0a:d5\n'
        # '  port=1, state=enabled, type=copper, speed=0 , portName=vxlan, portMac=46:7f:f4:82:e9:a0\n'
        # '  port=3, state=disabled, type=copper, speed=1000 , portName=eth1, portMac=08:00:27:7b:0a:d5\n\x1b[32m]',
        # '\x1b[0mports of:cafe000000000032\n'
        # 'id = of:cafe000000000032, available = true, role = MASTER, type = SWITCH, mfr = Nicira, Inc., hw = Open vSwitch, sw = 2.3.2, serial = None, managementAddress = 10.10.2.32, protocol = OF_13, driver = sona, name = of:cafe000000000033, channelId = 10.10.2.32:57373\n'
        # '  port = local, state=disabled, type = copper, speed = 0, portName=br-int, portMac = d2:84:d6:37:5f:4b\n'
        # '  port = 1, state=disabled, type = copper, speed = 0, portName=vxlan, portMac = 92:c4:a7:cd:29:7f\n\x1b[32m',
        # '\x1b[0mports of:cafe000000000033\n'
        # 'id = of:cafe000000000033, available = true, role = MASTER, type = SWITCH, mfr = Nicira, Inc., hw = Open vSwitch, sw = 2.3.2, serial = None, managementAddress = 10.10.2.33, protocol = OF_13, driver = sona, name = of:cafe000000000033, channelId = 10.10.2.33:52063\n'
        # '  port = local, state=enabled, type = copper, speed = 0, portName=aa, portMac = 1e:06:3a:1d:4a:41\n'
        # '  port = 1, state=disabled, type = copper, speed = 0, portName=vxlan, portMac = 92:4b:d6:25:e1:e5\n\x1b[32m']
        #

        for i in range(len(dev_list)):
            # print ('Devices(id : %s) : %s' %(dev_list[i]['id'], dev_list[i]['available']))
            if 'false' in dev_list[i]['available']:
                print 'device status ---------- nok'
                return False

            # port status
            # port_status = port_list[i]
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

        # print len(dev_list), br_int_status, vxlan_status

        print 'device status ---------- ok'
        if len(dev_list) != br_int_status:
            print 'port status(br-int) ---------- nok'
            return False

        if len(dev_list) != vxlan_status:
            print 'port status(vxlan) ---------- nok'
            return False

        print 'port status ---------- ok'

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
    def ssh_ping_test(cls, conn_info, dest):
        cmd = 'ping ' + dest + ' -c 3'
        recv_msg = cls.ssh_conn_send_command(conn_info, cmd)
        if recv_msg == False:
            return False

        print 'recv : ' + recv_msg
        # ping_list = recv_msg.splitlines()
        # print ping_list
        # split_list = ping_list[-3].split(', ')
        # print split_list
        # result = split_list[-2].split('%')
        # print result
        # if int(result[0]) != 0:
        #     print dest + ' ping test ---------------- nok'
        #     return False
        #
        # print dest + ' ping test ---------------- ok'
        return True

    @classmethod
    def ssh_ping_test2(cls, inst1, inst2, dest):
        cmd = 'ping ' + dest + ' -c 3'

        ssh_cmd = 'ssh cirros@192.168.0.8'
        # ssh_cmd = 'ssh' + inst2.username + '@' + inst2.hostname

        # conn = cls.ssh_connect('10.10.2.91', 'ina', '', 'telcowr1')
        conn = cls.ssh_connect(inst1.hostname, 'ina', '', 'telcowr1')
        if conn is False:
            return False

        conn.sendline(ssh_cmd)

        ssh_newkey = 'Are you sure you want to continue connecting'
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

        conn.sendline('cubswin:)')
        conn.expect(PROMPT, timeout=3)

        cls.change_prompt(conn)

        conn.sendline(cmd)
        conn.expect(CMD_PROMPT)

        # parsing loss rate
        ping_list = conn.before.splitlines()
        for list in ping_list:
            if 'loss' in list:
                split_list = list.split(', ')
                for x in split_list:
                    if '%' in x:
                        result = x.split('%')
                        # print result
                        break

        if int(result[0]) != 0:
            print dest + ' ping test ---------------- nok'
            return False

        print dest + ' ping test ---------------- ok'
        return True

    @classmethod
    def change_prompt(self, conn):
        change_cmd = "set prompt='[SONA]\# '"
        for i in range(2):
            try:
                conn.sendline(change_cmd)
                conn.expect(CMD_PROMPT, timeout=1)
                # print 'change prompt : ' + change_cmd
                break
            except Exception, e:
                # print e
                change_cmd = "PS1='[SONA]\# '"
                pass

