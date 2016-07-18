#
# kimjt Network temporarily test tool
#

from api.config import ReadConfig
from api.network import NetworkTester
from api.instance import InstanceTester
from api.reporter2 import Reporter

CONFIG_FILE = '../config/config.ini'

conf = ReadConfig(CONFIG_FILE)
test_network = NetworkTester(conf)
test_instance = InstanceTester(conf)
test_reporter = Reporter(conf)


# SONA Delete Test scenario
# =================================================================

# # Instance
# test_instance.delete_instance('instance1')
# test_instance.delete_instance('instance2')
# test_instance.delete_instance('instance3')
# test_instance.delete_instance('instance4')
#
# # Floating IP
# test_instance.delete_floatingip_all()
#
# # Security Group
# test_network.delete_seuritygroup('sg2')

# Router
test_network.remove_router_interface('router1', 'subnet2')
test_network.remove_router_interface('router1', 'subnet3')

test_network.delete_router('router1')

# Subnet
test_network.delete_subnet('subnet1')
test_network.delete_subnet('subnet2')
test_network.delete_subnet('subnet3')

# Network
test_network.delete_network('network1')
test_network.delete_network('network2')
test_network.delete_network('network3')

# =================================================================
test_reporter.test_summary()
