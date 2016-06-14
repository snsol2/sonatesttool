# Copyright 2016 Telcoware
# network control management classes

from neutronclient.v2_0 import client
from api.config import ReadConfig
import ast

# TODO
# apply oslo_log


class NetworkTester:

    def __init__(self, config_file):
        # Get config
        self.auth_conf = ReadConfig(config_file).get_auth_conf()
        self.network_conf = ReadConfig.get_network_config()
        self.subnet_conf = ReadConfig.get_subnet_config()
        # Get Token and Neutron Object
        self.neutron = client.Client(**self.auth_conf)

    # Get Networks Information
    # TODO
    # get_network_list_all and get_network_list merge
    def get_network_list_all(self):
        network_rst = self.neutron.list_networks()
        print "Network All List --->", dict(network_rst).values()
        return network_rst

    def get_network_list(self, network_opt):
        network_name = self.get_network_name(network_opt)
        network_rst = self.neutron.list_networks(name=network_name)
        print "Network List --->", network_opt, dict(network_rst).values()
        return network_rst

    def create_network(self, network_opt):
        network_body = dict(self.network_conf)[network_opt]
        # "ast.literal_eval" is to convert string type to dict type
        network_body = ast.literal_eval(network_body)
        network_rst = self.neutron.create_network(body=network_body)
        print "Network Create ---> Ok"
        return network_rst

    def delete_network(self, network_opt):
        network_uuid = self.get_network_uuid(network_opt)
        network_rst = self.neutron.delete_network(network_uuid)
        print "Delete network --->", network_opt, network_uuid
        return network_rst

    def update_network(self):
        pass

    def get_subnet_list_all(self):
        subnet_rst = self.neutron.list_subnets()
        print "Subnet All List --->", dict(subnet_rst).values()
        return subnet_rst

    def get_subnet_list(self, subnet_opt):
        subnet_name = self.get_subnet_name(subnet_opt)
        subnet_rst = self.neutron.list_subnets(name=subnet_name)
        print "Subnet List --->", subnet_opt, dict(subnet_rst).values()
        return subnet_rst

    def create_subnet(self, subnet_opt, network_opt):
        subnet_body = dict(self.subnet_conf)[subnet_opt]
        subnet_body = ast.literal_eval(subnet_body)
        network_uuid = self.get_network_uuid(network_opt)
        subnet_body['subnets'][0]['network_id'] = network_uuid
        subnet_rst = self.neutron.create_subnet(body=subnet_body)
        print "Create Subnet --->", network_opt, subnet_opt, dict(subnet_rst).values()
        return subnet_rst

    def delete_subnet(self):
        pass

    def update_subnet(self):
        pass

    def get_network_name(self, network_opt):
        network_conf = dict(self.network_conf)[network_opt]
        network_name = ast.literal_eval(network_conf)['network']['name']
        return network_name

    def get_network_uuid(self, network_opt):
        network_name = self.get_network_name(network_opt)
        network_rst = self.neutron.list_networks(name=network_name)
        network_uuid = dict(network_rst)['networks'][0]['id']
        return network_uuid

    def get_subnet_name(self, subnet_opt):
        subnet_conf = dict(self.subnet_conf)[subnet_opt]
        subnet_name = ast.literal_eval(subnet_conf)['subnets'][0]['name']
        return subnet_name

    def get_subnet_uuid(self, subnet_opt):
        subnet_name = self.get_subnet_name(subnet_opt)
        subnet_rst = self.neutron.list_subnets(name=subnet_name)
        subnet_uuid = dict(subnet_rst)['subnets'][0]['id']
        return subnet_uuid
