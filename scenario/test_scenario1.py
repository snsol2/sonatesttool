#
# kimjt Network temporarily test tool
#

from api.network import NetworkTester
from api.instance import InstanceTester
from api.reporter import Reporter
from api.ssh_util import SSHUtil
from api.ssh_tailer import SSHTailer
from api.config import ReadConfig
import time
import threading


CONFIG_FILE = '../config/config.ini'

test_network = NetworkTester(CONFIG_FILE)
test_instance = InstanceTester(CONFIG_FILE)
config = ReadConfig(CONFIG_FILE)
Reporter()

ssh_util = SSHUtil()
ssh_tail = SSHTailer()

ssh_tail.ssh_start_tailer()

ssh_util.ssh_ping('instance6', '', 'instance6:network5')
ssh_util.ssh_ping('instance6', 'instance1:network5', 'instance6:network5')
ssh_util.onos_application_status()
ssh_util.onos_devices_status()


#
for i in range(300):
    if i == 20:
        ssh_tail.ssh_stop_all_tailer('nok')

    if i == 25:
        break;

    if i > 10:
        print ('[%d][%d] : %s' % (i, threading.activeCount(), ssh_tail.thr_status_dic))

    time.sleep(1)

# SONA Test scenario
# Reference default Config
# =================================================================

# test_network.get_network('network3')
# test_network.get_network('network3')
# # test_instance.get_instance('instance1')
# # test_network.create_network('network3')
# # test_network.delete_network('network3')
#
# test_network.get_subnet('subnet3')
# test_network.create_subnet('subnet3', 'network3')
# # test_network.delete_subnet('subnet3')
# #
# # test_network.create_network('network2')
# # test_network.create_subnet('subnet2', 'network2')
# #
# # test_network.create_securitygroup('sg2', 'rule1,rule2')
# #
# #
# """
# CAUTION
# when create router, if external routing, second option must be external network.
#                     if not external routing, option is none('')
# """
# # test_network.create_router('router1', 'network1')
# # test_network.add_router_interface('router1', 'subnet2')
# #
# test_instance.create_instance('instance3', 'network3')
# # test_instance.delete_instance('instance3')
#
#
# # test_instance.floatingip_associate('instance1', 'ext-net')
# Reporter.test_summary()


# test_instance.floatingip_associate('instance1', 'ext-net')
Reporter.test_summary()
