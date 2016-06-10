# Copyright 2016 Telcoware
# network control management classes

from neutronclient.v2_0 import client

# TODO
# apply oslo_log

class Network:
    def __init__(self, auth_config):
        self.neutron = client.Client(**auth_config)

    def read_network_lists(self):
        networks = self.neutron.list_networks()
        return networks
