#!/usr/bin/python
#
# kimjt Network temporarily test tool
#

from api.sonatest import SonaTest

CONFIG_FILE = '../config/config.ini'

test = SonaTest(CONFIG_FILE)

# SONA Delete Test scenario
# =================================================================

# Instance
# test.instance.delete_instance('instance1')
# test.instance.delete_instance('instance2')
# test.instance.delete_instance('instance3')
# test.instance.delete_instance('instance4')

# Floating IP
test.instance.delete_floatingip_all()

# Security Group
test.network.delete_securitygroup('sg2')

# Router
test.network.remove_router_interface('router1', 'subnet2')
test.network.remove_router_interface('router1', 'subnet3')

test.network.delete_router('router1')

# Subnet
test.network.delete_subnet('subnet1')
test.network.delete_subnet('subnet2')
test.network.delete_subnet('subnet3')

# Network
test.network.delete_network('network1')
test.network.delete_network('network2')
test.network.delete_network('network3')

test.identity.delete_user()
# =================================================================
test.reporter.test_summary()
