import requests
import json
from api.reporter2 import Reporter

class ONOSInfo():
    _config=''

    def __init__(self, config):
        # print 'init'
        ONOSInfo._config = config

    def onos_create_session(self, conn_info):
        try:
            conn = requests.session()
            conn.auth = (conn_info['user'], conn_info['password'])
            return conn
        except:
            return

    def app_info(self, conn_info, app_name):
        try:
            conn = self.onos_create_session(conn_info)
            url = 'http://' + conn_info['host'] + ':8181/onos/v1/applications/' + app_name
            header = {'Accept': 'application/json'}
            # print json.dumps(conn.get(url, headers=header).json(),indent=4, separators=('',':'))
            return dict(conn.get(url, headers=header, timeout= self._config.get_onos_timeout()).json())['state'].encode('utf-8')
        except:
            return

    def device_info(self, conn_info):
        try:
            conn = self.onos_create_session(conn_info)
            url = 'http://' + conn_info['host'] + ':8181/onos/v1/devices/'
            header = {'Accept': 'application/json'}
            ret = json.dumps(conn.get(url, headers=header, timeout= self._config.get_onos_timeout()).json(), ensure_ascii=False, sort_keys=False).encode('utf-8')
            dev_list = json.loads(ret)
            return dev_list['devices']
        except:
            return

    def port_info(self, conn_info, dev_id):
        try:
            conn = self.onos_create_session(conn_info)
            url = 'http://' + conn_info['host'] + ':8181/onos/v1/devices/' + dev_id + '/ports'
            header = {'Accept': 'application/json'}
            # print json.dumps(conn.get(url, headers=header).json(),indent=4, separators=('',':'))
            ret = json.dumps(conn.get(url, headers=header, timeout= self._config.get_onos_timeout()).json(), ensure_ascii=False, sort_keys=False).encode('utf-8')
            port_list = json.loads(ret)

            result = []
            for x in dict(port_list)['ports']:
                port_name = dict(dict(x)['annotations'])
                port_status = dict(x)
                # test
                # if 'vxlan' in port_name['portName']:
                #     port_status['isEnabled'] = False
                result.append({port_name['portName'] : port_status['isEnabled']})

            return result
        except:
            return

    def device_status(self, conn_info):
        try:
            dev_list = self.device_info(conn_info)
            if None is dev_list:
                return False

            br_int_status = 0
            vxlan_status = 0
            dev_cnt = 0
            for i in range(len(dev_list)):
                dev_info_dic = dict(dev_list[i])
                proto = dict(dev_info_dic['annotations']).get('protocol')
                if None is proto:
                    continue
                dev_cnt += 1
                Reporter.REPORT_MSG('   >>[%d] %s', i, dev_info_dic)
                if False is dev_info_dic['available']:
                    Reporter.REPORT_MSG('   >> [%s] device[%s] status nok', conn_info['host'], dev_info_dic['id'])
                    return False

                # Port status(br-int)
                port_result = self.port_info(conn_info, dev_info_dic['id'])
                status = 0
                for x in port_result:
                    str = dict(x)
                    if str.has_key('br-int') == True :
                        status = 1
                        break
                br_int_status += status

                # Port status(vxlan)
                for x in port_result:
                    str = dict(x)
                    if str.has_key('vxlan') == True:
                        if True is str['vxlan']:
                            vxlan_status += 1

            # br-int
            if dev_cnt != br_int_status:
                Reporter.REPORT_MSG('   >> [%s] port status(br-int) -- nok', conn_info['host'])
                return False

            # vxlan-int
            if dev_cnt != vxlan_status:
                Reporter.REPORT_MSG('   >> [%s] port status(vxlan)  -- nok', conn_info['host'])
                return False

            Reporter.REPORT_MSG('   >> [%s] device, port status -- ok', conn_info['host'])
            return True
        except:
            Reporter.exception_err_write()

    def application_status(self, report_flag=None):
        if report_flag is None:
            Reporter.unit_test_start(True)
        try:
            onos_info = self._config.get_onos_info()
            state_list=[]
            conn_info = {}
            state_info = {}
            for onos_ip in onos_info.onos_list:
                conn_info['host'] = onos_ip
                conn_info['user'] = onos_info.user_id
                conn_info['password'] = onos_info.password

                ret = self.app_info(conn_info, 'org.onosproject.openstackswitching')
                state_info['openstackswitching'] = ret; state_list.append(ret)
                ret = self.app_info(conn_info, 'org.onosproject.openstackrouting')
                state_info['openstackrouting'] = ret; state_list.append(ret)
                ret = self.app_info(conn_info, 'org.onosproject.openstacknetworking')
                state_info['openstacknetworking'] = ret; state_list.append(ret)
                ret = self.app_info(conn_info, 'org.onosproject.openstacknode')
                state_info['openstacknode'] = ret; state_list.append(ret)
                ret = self.app_info(conn_info, 'org.onosproject.openstackinterface')
                state_info['openstackinterface'] = ret; state_list.append(ret)

                if 'ACTIVE' in state_list:
                    Reporter.REPORT_MSG('   >> [%s][Application OK] : %s', onos_ip, state_info)
                else:
                    Reporter.REPORT_MSG('   >> [%s][Application NOK] : %s', onos_ip, state_info)
                    if report_flag is None:
                        Reporter.unit_test_stop('nok')
                        return False

            if report_flag is None:
                Reporter.unit_test_stop('ok')

            return True
        except:
            # Reporter.exception_err_write()
            return False

    def devices_status(self, report_flag=None):
        if report_flag is None:
            Reporter.unit_test_start(True)
        try:
            onos_info = self._config.get_onos_info()
            conn_info = {}
            for onos_ip in onos_info.onos_list:
                conn_info['host'] = onos_ip
                conn_info['user'] = onos_info.user_id
                conn_info['port'] = onos_info.ssh_port
                conn_info['password'] = onos_info.password
                ret = self.device_status(conn_info)
                if False is ret:
                    if report_flag is None:
                        Reporter.unit_test_stop('nok')
                        return False

            if report_flag is None:
                Reporter.unit_test_stop('ok')
            return True
        except:
            # Reporter.exception_err_write()
            return False
