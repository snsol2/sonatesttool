from neutronclient.v2_0 import client
from api.config import ReadConfig
import json
import ast

# TODO
# - apply oslo_log
# - Exception


auth_conf = ReadConfig('../config/config.ini').get_net_auth_conf()
neutron = client.Client(**auth_conf)




body1 = {"security_group": {'name': 'new-sg'}}

body = {'security_group': {'name': 'new-sg', 'description': 'Test Tool SG'},
        'security_group_rule': [{'direction': 'ingress',
                                 'port_range_min': '80',
                                 'ethertype': 'IPv4',
                                 'port_range_max': '80',
                                 'protocol': 'tcp'},
                                {'direction': 'egress',
                                 'port_range_min': '80',
                                 'ethertype': 'IPv4',
                                 'port_range_max': '80',
                                 'protocol': 'tcp'}]}

# print type(body1)
# neutron.create_security_group(body1)

# print json.dumps(dict(neutron.list_security_groups())['security_groups'][1], indent=4, separators=(',',':'))
# print len(dict(neutron.list_security_groups())['security_groups'])


# class NetworkTester:
#
#     def __init__(self, config_file):
#         # Get config
#         self.auth_conf = ReadConfig(config_file).get_net_auth_conf()
#         self.network_conf = ReadConfig.get_network_config()
#         self.subnet_conf = ReadConfig.get_subnet_config()
#         # Get Token and Neutron Object
#         self.neutron = client.Client(**self.auth_conf)

# aaa = [{1: 'test1'}, {2: 'test2'}, {3: 'test3'}, {4: 'teset4'}]
# aaa = ['aa', 'bb', 'cc']
# # aaa = [1, 2, 3]
# print aaa[:]

# bbb = [ip['ip_address'] for ip in aaa]
# print bbb
# class bcolors:
#     HEADER='\033[95m'
#     OKBLUE='\033[94m'
#     OKGREEN='\033[92m'
#     WARNING='\033[93m'
#     FAIL='\033[91m'
#     ENDC='\033[0m'
#     BOLD='\033[1m'
#     UNDERLINE='\033[4m'
#
# print bcolors.BOLD
# print bcolors.WARNING
# print "Warning:Noactivefrommetsremain.Continue?" # +bcolors.ENDC
# print 'asdfadf'

print "%s aassssdfa %s"
