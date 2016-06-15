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
test_network.get_network_list('network3')

# test_network.create_network('network1')

# test_network.delete_network('network2')


# test_network.get_subnet_list_all()
# test_network.get_subnet_list('subnet2')
# test_network.create_subnet('subnet1', 'network1')
# test_network.delete_subnet('subnet1')
test_network.get_subnet_list('subnet1')



