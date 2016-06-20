#
# kimjt Network temporarily test tool
#

from api.network import NetworkTester

CONFIG_FILE = '../config/config.ini'

test_network = NetworkTester(CONFIG_FILE)

# SONA Test scenario
# Reference default Config
# Network ]
# =================================================================

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
