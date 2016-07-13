#
# kimjt Network temporarily test tool
#

from api.network import NetworkTester
from api.instance import InstanceTester
from api.reporter import Reporter

CONFIG_FILE = '../config/config.ini'

test_network = NetworkTester(CONFIG_FILE)
test_instance = InstanceTester(CONFIG_FILE)
Reporter()


# SONA Test scenario
# Reference default Config
# =================================================================

# test_network.get_network('network3')
# test_network.get_subnet('subnet3')
### Network
test_network.create_network('network3')
# test_network.delete_network('network3')

test_network.create_subnet('subnet3', 'network3')
# test_network.delete_subnet('subnet3')

# test_network.create_network('network2')
# test_network.create_subnet('subnet2', 'network2')

# test_network.create_router('router3', 'network1')
# test_network.delete_router('router2')
# test_network.add_router_interface('router3', 'subnet3')
# test_network.remove_router_interface('router3', 'subnet3')

# test_network.get_sg_uuid('sg2')
# test_network.create_securitygroup('sg2', 'rule1,rule2')


test_instance.create_instance('instance3', 'network3')
test_instance.delete_instance('instance3')

# test_instance.floatingip_associate('instance1', 'ext-net')

# test_network.set_port_down('instance1', 'network2')
# test_network.set_port_up('instance1', 'network2')

# test_network.set_router_down('router3')
# test_network.set_router_up('router3')
Reporter.test_summary()

# test_network.test()
