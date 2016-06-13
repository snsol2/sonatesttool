#
# kimjt Network temporarily test tool
#

from api.config import ReadConfig
from api.network import Network

CONFIG_PATH = '../config/'
CONFIG_FILE = 'config.ini'

config = ReadConfig(CONFIG_PATH + CONFIG_FILE)

auth_config = config.get_auth_conf()

# network_config1 = config.get_network_conf()
# [network_config1, network_config2] = config.get_network_conf()
# [network_config1, network_config2, network_config3] = config.get_network_conf()
network_config = list(config.get_network_conf())


# network = Network(auth_config)

# print dict(auth_config)
# print network_config1

for a in network_config:
    print dict(a)
    # print dict(a['network'])


# print dict(network_config1[0])['network']
# print dict(network_config1[1])['subnet']
# print dict(network_config1[2])['network']
# print dict(network_config2)
# print dict(network_config3)


# print (network.read_network_lists())




