
from api.config import ReadConfig
from api.network import Network
import json

CONFIG_PATH = '../config/'
CONFIG_FILE = 'config.ini'

auth_config = ReadConfig(CONFIG_PATH + CONFIG_FILE).get_auth_conf()

network = Network(auth_config)


print json.dumps(network.read_network_lists(), indent=4, separators=(',',':'))



