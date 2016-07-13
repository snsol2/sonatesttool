#
# kimjt Network temporarily test tool
#

from api.instance import InstanceTester

CONFIG_FILE = '../config/config.ini'
EXT_NETWORK = 'ext-net'

test_instance = InstanceTester(CONFIG_FILE)

# SONA Test scenario
# Reference default Config
# Network ]
# =================================================================

print "Test Start ===="
print "----------------------------"

# test_instance.get_server_list_all()
import json
print test_instance.get_instance('instance1')[0].id
# test_instance.create_instance('instance1', 'network2, network3')
# test_instance.create_instance('instance1', 'network2')
# test_instance.delete_instance('instance1')

test_instance.get_floatingip_list()
# test_instance.floatingip_associate('instance1', EXT_NETWORK)

# test_instance.floatingip_separate('instance1')
# test_instance.delete_floatingip_all()

test_instance.get_instance_floatingip('instance1')
