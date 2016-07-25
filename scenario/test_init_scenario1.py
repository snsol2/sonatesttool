#
# SONA temporarily test tool
#        Telcoware 2016/7/25
#

from api.sonatest import SonaTest
CONFIG_FILE = '../config/config.ini'

test = SonaTest(CONFIG_FILE)


# SONA Test scenario
# =================================================================
# status check
test.onos_and_openstack_check()

# # Network
# test.network.create_network('network1')
# test.network.create_network('network2')
# test.network.create_network('network3')
#
# # Subnet
# test.network.create_subnet('subnet1', 'network1')
# test.network.create_subnet('subnet2', 'network2')
# test.network.create_subnet('subnet3', 'network3')
#
# # Router
# test.network.create_router('router1', 'network1')
# test.network.add_router_interface('router1', 'subnet2')
# test.network.add_router_interface('router1', 'subnet3')
#
# # Security Group
# test.network.create_securitygroup('sg2', 'rule1,rule2')

# Instance
test.instance.create_instance('instance1', 'network2', 'sg2')
test.instance.create_instance('instance2', 'network2', '')
test.instance.create_instance('instance3', 'network3', 'sg2')
test.instance.create_instance('instance4', 'network3', '')
#
# # Floating IP
# test.floating_ip_check('instance1')
# test.instance.floatingip_associate('instance1', 'ext-net')
# test.ssh_ping('instance1', '', 'instance2:network2')
# test.ssh_ping('instance1', 'instance2:network2', '10.10.2.103')
# =================================================================
test.reporter.test_summary()
