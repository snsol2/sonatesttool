#
# kimjt Network temporarily test tool
#

from api.network import NetworkTester
from api.instance import InstanceTester
from api.reporter import Reporter
from api.reporter2 import Reporter
from api.ssh_util import Status
from api.config import ReadConfig
from api.ssh_tailer import tailer
import threading
import time

CONFIG_FILE = '../config/config.ini'

config = ReadConfig(CONFIG_FILE)
test_network = NetworkTester(config)
test_instance = InstanceTester(config)
# Reporter()



Reporter(config)
ssh_util = Status(config)
# print datetime.datetime.now().time()
# ssh_util.onos_application_status()
ssh_util.onos_devices_status()
# ssh_util.ssh_ping('instance6', '', '10.10.2.93')
#
# ssh_tailer = tailer()
# ssh_tailer.start_tailer()
# # print datetime.datetime.now().time()
#
# log.unit_test_start()
# for i in range(100):
#     if i==10:
#         log.unit_test_stop('nok')
#         break
#     #
#     print ('[%d][%d] : %s' %(i, threading.activeCount(), Reporter.thr_status_dic))
#     time.sleep(1)

  # print ssh_tt.join_list, ssh_tt.thr_list

  # for thr in ssh_tt.join_list:
      # thr.join(1)
      # ssh_tt.join_list.remove(thr)
      # ssh_tt.thr_list.remove(thr)



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
