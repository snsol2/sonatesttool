# Copyright 2016 Telcoware

from neutronclient.v2_0 import client
from config import ReadConfig

CONFIG_FILE = '../config/config.ini'

auth_config = ReadConfig(CONFIG_FILE)
neutron = client.Client(**auth_config.get_auth_conf())
networks = neutron.list_networks()

# print json.dumps(networks, indent=4, separators=(',',':'))

print networks
