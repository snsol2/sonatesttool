#!/usr/bin/python
#
# kimjt Network temporarily test tool
#

from api.network import NetworkTester
from api.config import ReadConfig

CONFIG_FILE = '../config/config.ini'
cfg = ReadConfig(CONFIG_FILE)
# test_network = NetworkTester(CONFIG_FILE)


import ConfigParser
import collections

# net_items = collections.OrderedDict()
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)
# print config.get("network","network1")
net_items =  config._sections['network']
print len(net_items)
print net_items['network1']
# net_items.keys().index('network1')
# foodIndex = {k:i for i,k in enumerate(net_items.keys())}
# print foodIndex
# print net_items
# for key, path in net_items:
#     print key,'=', path
# # net_items = config.items("network")
# for key, path in net_items:
#     print key,'=', path

# SONA Test scenario
# Reference default Config
# Network ]
# =================================================================

# print "Test Start ===="
# print "----------------------------"a
# test = cfg.get_section_test()
# print dict(test)
# test_network.get_network('network3')
# test_network.create_network('network1')
# test_network.create_network('network3')
# test_network.delete_network('network3')
# test_network.get_network_uuid('network3')


# test_network.get_subnet_lists()
# test_network.get_subnet('subnet4')
# test_network.get_subnet_uuid('subnet2')
# test_network.create_subnet('subnet1', 'network1')
# test_network.create_subnet('subnet2', 'network3')
# test_network.delete_subnet('subnet2')

# test_network.get_securitygroup_lists()
# test_network.get_securitygroup('sg2')
# test_network.get_sg_uuid('sg2')
# test_network.create_securitygroup('sg2', 'rule1,rule4')
# test_network.delete_seuritygroup('sg2')

# test_network.get_router_lists()
# test_network.get_router('router1')

# ## create_router CAUTION
# ## when create router, if for external routing, second option must be external network.
# ##                     if not for external, option is none
# test_network.create_router('router1', 'network1')
# test_network.create_router('router1', '')
# test_network.delete_router('router1')

# test_network.add_router_interface('router1', 'subnet2')
# test_network.remove_router_interface('router1', 'subnet2')

# test_network.set_port_down('instance1', 'network2')
# test_network.set_port_up('instance1', 'network2')

# test_network.set_network_down('network2')
# test_network.set_network_up('network2')
