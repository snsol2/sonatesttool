#
# kimjt Network temporarily test tool
#

from api.network import NetworkTester
from api.instance import InstanceTester
from api.reporter import Reporter
from api.ssh_util import SSHUtil

CONFIG_FILE = '../config/config.ini'

test_network = NetworkTester(CONFIG_FILE)
test_instance = InstanceTester(CONFIG_FILE)
test_status = SSHUtil()
Reporter()


# SONA Test scenario
# =================================================================
# status check
test_status.onos_application_status()
test_status.onos_devices_status()

# # Network
# test_network.create_network('network1')
# test_network.create_network('network2')
# test_network.create_network('network3')
#
# # Subnet
# test_network.create_subnet('subnet1', 'network1')
# test_network.create_subnet('subnet2', 'network2')
# test_network.create_subnet('subnet3', 'network3')
#
# # Router
# test_network.create_router('router1', 'network1')
# test_network.add_router_interface('router1', 'subnet2')
# test_network.add_router_interface('router1', 'subnet3')
#
# # Security Group
# test_network.create_securitygroup('sg2', 'rule1,rule2')
#
# # Instance
# test_instance.create_instance('instance1', 'network2')
# test_instance.create_instance('instance2', 'network2')
# test_instance.create_instance('instance3', 'network3')
# test_instance.create_instance('instance4', 'network3')
#
# # Floating IP
# test_instance.floatingip_associate('instance1', 'ext-net')

# =================================================================
Reporter.test_summary()

