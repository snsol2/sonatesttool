#
# kimjt Network temporarily test tool
#
from api.network import NetworkTester
from api.reporter import CLog
import datetime
from api.config import ReadConfig

CONFIG_FILE = '../config/config.ini'

now = datetime.datetime.now()
now_time = now.strftime('%Y-%m-%d')
file_name = ReadConfig(CONFIG_FILE).get_file_path() + '/REPORT_' + now_time
LOG = CLog(file_name)


test_network = NetworkTester(CONFIG_FILE)

# SONA Test scenario
# Reference default Config
# Network ]
# =================================================================
test_network.get_network_log_test()

msg1 = 'args1'
msg2 = 'args2'
LOG.REPORT_MSG('Report %s, %s test', msg1, msg2)
LOG.PRINTR('ttttaaaa %s, %s blue', msg1, msg2)
LOG.PRINTG('ttttaaaa %s, %s blue', msg1, msg2)
LOG.PRINTB('ttttaaaa %s, %s blue', msg1, msg2)
LOG.PRINTY('ttttaaaa %s, %s blue', msg1, msg2)

LOG.NRET_PRINT('return :'), LOG.PRINTR('%s', msg1)
LOG.NRET_PRINT('return :'), LOG.RESULT_PRINT('OK');


print "Test Start ===="
print "----------------------------"
# test_network.get_network_list_all()
# test_network.get_network_list('network3')
# test_network.create_network('network1')
# test_network.create_network('network2')
# test_network.delete_network('network2')


# test_network.get_subnet_list_all()
# test_network.get_subnet_list('subnet2')
# test_network.create_subnet('subnet1', 'network1')
# test_network.create_subnet('subnet2', 'network2')
# test_network.delete_subnet('subnet1')

# test_network.get_securitygroup_list_all()
# test_network.get_securitygroup_list('sg1')
# test_network.create_securitygroup('sg2', 'rule1,rule2')

# test_network.delete_seuritygroup('sg2')

# test_network.get_router_list_all()
# test_network.get_router_list('router1')

# ## create_router CAUTION
# ## when create router, if for external routing, second option must be external network.
# ##                     if not for external, option is none
# test_network.create_router('router1', 'network1')
# test_network.create_router('router1', '')
# test_network.delete_router('router1')

# test_network.add_router_interface('router1', 'subnet2')
# test_network.remove_router_interface('router1', 'subnet2')
