#
# kimjt Network temporarily test tool
#

from api.config import ReadConfig
from api.network import Network

CONFIG_PATH = '../config/'
CONFIG_FILE = 'config.ini'

config = ReadConfig(CONFIG_PATH + CONFIG_FILE)

auth_config = config.get_auth_conf()
network_config = config.get_network_conf()


network = Network(auth_config)

print dict(network_config)


print type(network.read_network_lists())




