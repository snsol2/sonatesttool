# Copyright 2016 Telcoware
# network control management classes

from novaclient import client
from api.config import ReadConfig


class InstanceTester:

    def __init__(self, config_file):
        # Get config
        self.auth_conf = ReadConfig(config_file).get_nova_auth_conf()
        self.network_conf = ReadConfig.get_network_config()
        self.subnet_conf = ReadConfig.get_subnet_config()
        # Get Token and Neutron Object
        self.neutron = client.Client(**self.auth_conf)


