#
# kimjt Network temporarily test tool
#

from api.instance import InstanceTester

CONFIG_FILE = '../config/config.ini'

test_instance = InstanceTester(CONFIG_FILE)

# SONA Test scenario
# Reference default Config
# Network ]
# =================================================================

print "Test Start ===="
print "----------------------------"

# test_instance.get_server_list_all()

# test_instance.get_instance_list('instance1')
test_instance.create_instance('instance2')
