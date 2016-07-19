#
# kimjt Network temporarily test tool
#

from api.config import ReadConfig
from api.network import NetworkTester
from api.instance import InstanceTester
from api.reporter2 import Reporter
from api.state import State

CONFIG_FILE = '../config/config.ini'

conf = ReadConfig(CONFIG_FILE)
test_network = NetworkTester(conf)
test_instance = InstanceTester(conf)
test_status = State(conf)
test_reporter = Reporter(conf)


# SONA Test scenario
# =================================================================
# status check
test_status.onos_application_status()
test_status.onos_devices_status()
test_status.openstack_get_token()
test_status.openstack_get_service()

# Network
test_network.create_network('network1')
test_network.create_network('network2')
test_network.create_network('network3')

# Subnet
test_network.create_subnet('subnet1', 'network1')
test_network.create_subnet('subnet2', 'network2')
test_network.create_subnet('subnet3', 'network3')

# Router
test_network.create_router('router1', 'network1')
test_network.add_router_interface('router1', 'subnet2')
test_network.add_router_interface('router1', 'subnet3')

# Security Group
test_network.create_securitygroup('sg2', 'rule1,rule2')

# Instance
test_instance.create_instance('instance1', 'network2', 'sg2')
test_instance.create_instance('instance2', 'network2', '')
test_instance.create_instance('instance3', 'network3', 'sg2')
test_instance.create_instance('instance4', 'network3', '')

# Floating IP
test_instance.floatingip_associate('instance1', 'ext-net')

test_status.ssh_ping('instance1','', '10.10.2.93')
test_status.ssh_ping('instance1','instance2:network2', '10.10.2.93')
# =================================================================
test_reporter.test_summary()

