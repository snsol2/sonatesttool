#
# kimjt Network temporarily test tool
#

from api.network import NetworkTester
from api.instance import InstanceTester
from api.reporter import Reporter

CONFIG_FILE = 'config/config.ini'
EXT_NETWORK = 'ext-net'

test_network = NetworkTester(CONFIG_FILE)
test_instance = InstanceTester(CONFIG_FILE)
clog = Reporter()


# SONA Test scenario
# Reference default Config
# =================================================================

print("Test Start ====")
print("----------------------------")
test_network.get_network('network1')
test_instance.get_instance('instance1')
# test_network.create_network('network4')
# test_network.create_subnet('subnet1', 'network1')
#
# test_network.create_network('network2')
# test_network.create_subnet('subnet2', 'network2')
#
# test_network.create_securitygroup('sg2', 'rule1,rule2')
#
#
# # ## create_router CAUTION
# # ## when create router, if for external routing, second option must be external network.
# # ##                     if not for external, option is none
# test_network.create_router('router1', 'network1')
# test_network.add_router_interface('router1', 'subnet2')
#
test_instance.create_instance('instance1', 'network2')


# test_instance.floatingip_associate('instance1', EXT_NETWORK)
