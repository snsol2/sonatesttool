# Copyright 2016 Telcoware
# network control management classes

from neutronclient.v2_0 import client
from api.config import ReadConfig
from api.instance import InstanceTester
from api.reporter import Reporter
import ast
import traceback
import sys

# TODO
# - apply log
# - Exception
# asdf


class NetworkTester:

    def __init__(self, config_file):
        # Get config
        # CLog.__init__(self, config_file)
        self.auth_conf = ReadConfig(config_file).get_net_auth_conf()
        self.network_conf = ReadConfig.get_network_config()
        self.subnet_conf = ReadConfig.get_subnet_config()
        self.sg_conf = ReadConfig.get_sg_config()
        self.rule_conf = ReadConfig.get_rule_config()
        self.router_conf = ReadConfig.get_router_config()
        # Get Token and Neutron Object
        self.neutron = client.Client(**self.auth_conf)
        # Get Token and Nova Object
        self.nova = InstanceTester(config_file)

    #
    # Networks Methods
    # TODO
    # - get_network_list_all and get_network_list merge
    def get_network_lists(self):
        network_rst = self.neutron.list_networks()
        if not network_rst:
            print 'Not exist Network --->'
            return
        # print "Network All List --->", dict(network_rst).values()
        return network_rst

    def get_network(self, network_opt):
        try:
            network_name = self.get_network_name(network_opt)
            if not network_name:
                return
            network_rst = self.neutron.list_networks(name=network_name)
            Reporter.REPORT_MSG("Network List ---> %s %s", network_opt, dict(network_rst).values())
            return network_rst
        except:
            Reporter.exception_err_write()

    def get_network_name(self, network_opt):
        network_body = dict(self.network_conf)[network_opt]
        if not network_body:
            print 'Not Exist Network in Config --->', network_opt
            return
        network_name = ast.literal_eval(network_body)['name']
        return network_name

    def get_network_uuid(self, network_opt):
        network_name = self.get_network_name(network_opt)
        if not network_name:
            return
        network_rst = self.neutron.list_networks(name=network_name)
        if not dict(network_rst)['networks']:
            print 'Not Exist Network on OpenStack --->'
            return
        network_uuid = dict(network_rst)['networks'][0]['id']
        return network_uuid

    def create_network(self, network_opt):
        # Reporter.unit_test_start()
        try:
            network_body = dict(self.network_conf)[network_opt]
            if not network_body:
                print 'Not Exist Network in Config'
                return

            if self.get_network_uuid(network_opt):
                print 'Already Exist same Network name --->'

            network_body = ast.literal_eval("{'network': " + network_body + "}")
            network_rst = self.neutron.create_network(body=network_body)
            print "Create Network--->", network_opt, dict(network_rst).values()
            return network_rst
        except:
            Reporter.exception_err_write()

    def delete_network(self, network_opt):
        network_uuid = self.get_network_uuid(network_opt)
        network_rst = self.neutron.delete_network(network_uuid)
        print "Delete Network --->", network_opt, network_uuid
        return network_rst

    # TODO
    def update_network(self):
        pass

    #
    # Subnet Methods
    #
    def get_subnet_lists(self):
        subnet_rst = self.neutron.list_subnets()
        if not subnet_rst:
            print 'Not Exist Subnet --->'
            return

        print "Subnet All List --->", dict(subnet_rst).values()
        return subnet_rst

    def get_subnet(self, subnet_opt):
        subnet_name = self.get_subnet_name(subnet_opt)
        if not subnet_name:
            print 'Not Exist Subnet in Config --->'
            return

        subnet_rst = self.neutron.list_subnets(name=subnet_name)
        if not subnet_rst:
            print 'Not Exist Subnet --->', subnet_name
            return

        print "Subnet List --->", subnet_opt, dict(subnet_rst).values()
        return subnet_rst

    def get_subnet_name(self, subnet_opt):
        subnet_conf = dict(self.subnet_conf)[subnet_opt]
        if not subnet_conf:
            print 'Not Exist Subnet in config --->'
            return

        subnet_name = ast.literal_eval(subnet_conf)['name']
        return subnet_name

    def get_subnet_uuid(self, subnet_opt):
        subnet_name = self.get_subnet_name(subnet_opt)
        if not subnet_name:
            return
        subnet_rst = self.neutron.list_subnets(name=subnet_name)
        if not dict(subnet_rst)['subnets']:
            print 'Not Exist Subnet --->'
            return
        subnet_uuid = dict(subnet_rst)['subnets'][0]['id']
        return subnet_uuid

    def create_subnet(self, subnet_opt, network_opt):
        subnet_body = dict(self.subnet_conf)[subnet_opt]
        if not subnet_body:
            print 'Not Exist Subnet in config --->'
            return

        if self.get_subnet_uuid(subnet_opt):
            print 'Already Exist same Subnet name --->'
            return

        subnet_body = ast.literal_eval("{'subnets': [" + subnet_body + "]}")

        network_uuid = self.get_network_uuid(network_opt)
        if not network_uuid:
            print 'Not Exist Network --->'
            return

        subnet_body['subnets'][0]['network_id'] = network_uuid
        subnet_rst = self.neutron.create_subnet(body=subnet_body)
        print "Create Subnet --->", network_opt, subnet_opt, dict(subnet_rst).values()
        return subnet_rst

    def delete_subnet(self, subnet_opt):
        subnet_uuid = self.get_subnet_uuid(subnet_opt)
        if not subnet_uuid:
            return

        subnet_rst = self.neutron.delete_subnet(subnet_uuid)
        print "Delete network --->", subnet_opt, subnet_uuid
        return subnet_rst

    # TODO
    def update_subnet(self):
        pass

    #
    # Security Group Methods
    #
    def get_securitygroup_lists(self):
        sg_rst = self.neutron.list_security_groups()
        print 'SecurityGroup list --->', dict(sg_rst)
        return sg_rst

    def get_securitygroup(self, sg_opt):
        sg_name = self.get_sg_name(sg_opt)
        sg_rst = self.neutron.list_security_groups(name=sg_name)
        print 'SecurityGroup list --->', sg_opt, dict(sg_rst)
        return sg_rst

    def get_sg_name(self, sg_opt):
        sg_conf = dict(self.sg_conf)[sg_opt]
        if not sg_conf:
            print 'Not Exist config file --->', sg_opt
            return

        sg_name = ast.literal_eval(sg_conf)['name']
        return sg_name

    def get_sg_uuid(self, sg_opt):
        sg_name = self.get_sg_name(sg_opt)
        if not sg_name:
            return

        sg_rst = self.neutron.list_security_groups(name=sg_name)
        if not sg_rst['security_groups']:
            print 'Not Exist Security Group in OpenStack --->', sg_opt, sg_name
            return

        sg_uuid = []
        for i in range(len(sg_rst['security_groups'])):
            sg_uuid.append(dict(sg_rst)['security_groups'][i]['id'])

        return sg_uuid

    def create_securitygroup(self, sg_opt, rule_opt_list):
        if not self.get_sg_name(sg_opt):
            return
        if self.get_sg_uuid(sg_opt):
            print 'Already Exist Security Group --->', sg_opt
            return

        sg_body = dict(self.sg_conf)[sg_opt]
        sg_body = ast.literal_eval("{'security_group': " + sg_body + "}")

        # Create New Security Group
        sg_rst = self.neutron.create_security_group(sg_body)
        print 'Create Security Group --->', sg_rst

        # Make Rule to Security Group
        rule_rst = self.add_securitygroup_rule(sg_rst['security_group']['id'],
                                               rule_opt_list.split(','))
        if not rule_rst:
            print 'Make Rule Error'
            self.delete_seuritygroup(sg_opt)
            return

        print 'Make Rule Succ --->', rule_rst
        return rule_rst

    def add_securitygroup_rule(self, sg_uuid, rule_opt_list):
        rule_rst = []
        for rule in rule_opt_list:
            rule_conf = dict(self.rule_conf)[rule.strip()]
            if not rule_conf:
                print 'Not Exist Rule --->', rule
                return
            rule_body = ast.literal_eval(rule_conf)
            rule_body['security_group_id'] = sg_uuid
            rule_body = {'security_group_rule': rule_body}
            rule_rst.append(self.neutron.create_security_group_rule(rule_body))
        print 'Security Group', rule_rst
        return rule_rst

    def delete_seuritygroup(self, sg_opt):
        sg_uuid = self.get_sg_uuid(sg_opt)
        if not sg_uuid:
            return

        sg_rst = []
        for uuid in sg_uuid:
            sg_rst.append(self.neutron.delete_security_group(uuid))

        print 'Delete Security Group Succ --->', sg_opt, sg_rst
        return sg_rst

    #  TODO
    def update_securitygroup(self):
        pass

    #
    # Router Control Method
    #
    def get_router_list_all(self):
        router_rst = self.neutron.list_routers()
        print 'Router List --->', router_rst
        return router_rst

    def get_router_list(self, router_opt):
        router_name = self.get_router_name(router_opt)
        if not router_name:
            return

        router_rst = self.neutron.list_routers(name=router_name)
        # print 'Router list --->', router_rst
        return router_rst

    def get_router_name(self, router_opt):
        router_conf = dict(self.router_conf)[router_opt]
        if not router_conf:
            print 'Not Exist config file --->', router_opt
            return
        router_name = ast.literal_eval(router_conf)['router']['name']
        return router_name

    def get_router_uuid(self, router_opt):
        router_rst = self.get_router_list(router_opt)
        router_uuid = router_rst['routers'][0]['id']
        return router_uuid

    def create_router(self, router_opt, network_opt):
        router_body = ast.literal_eval(dict(self.router_conf)[router_opt])
        if not router_body:
            print 'Not Exist config file --->', router_opt
            return

        if network_opt:
            network_uuid = self.get_network_uuid(network_opt)
            if not network_uuid:
                return
            router_body['router']['external_gateway_info'] = {'network_id': network_uuid}

        router_rst = self.neutron.create_router(router_body)
        print 'Create Router --->', router_rst
        return router_rst

    def delete_router(self, router_opt):
        router_uuid = self.get_router_uuid(router_opt)
        router_rst = self.neutron.delete_router(router_uuid)
        print 'Delete Router --->', router_rst

    def add_router_interface(self, router_opt, subnet_opt):
        router_uuid = self.get_router_uuid(router_opt)
        subnet_uuid = self.get_subnet_uuid(subnet_opt)

        if subnet_uuid and router_uuid:
            router_if_body = {'subnet_id': subnet_uuid}
            router_if_rst = self.neutron.add_interface_router(router_uuid, router_if_body)
            print 'Add Router Interface --->', router_if_rst
            return router_if_rst
        return

    def remove_router_interface(self, router_opt, subnet_opt):
        router_uuid = self.get_router_uuid(router_opt)
        subnet_uuid = self.get_subnet_uuid(subnet_opt)

        if subnet_uuid and router_uuid:
            router_if_body = {'subnet_id': subnet_uuid}
            router_if_rst = self.neutron.remove_interface_router(router_uuid, router_if_body)
            print 'Remove Router Interface --->', router_if_rst
            return router_if_rst
        return

    def get_port_uuid(self, instance_opt, network_opt):
        instance_uuid = self.nova.get_instance(instance_opt)[0].id
        if not instance_uuid:
            return
        network_uuid = self.get_network_uuid(network_opt)
        if not network_uuid:
            return

        port_id_map = [(a['id'], a['device_id'])
                       for a in dict(self.neutron.list_ports(network_id=network_uuid))['ports']]

        port_id_map = dict(map(reversed, port_id_map))

        port_uuid = []
        for k in port_id_map.keys():
            if k == instance_uuid:
                port_uuid.append(port_id_map[k])

        return port_uuid

    def set_port_down(self, instance_opt, network_opt):
        body = {'port': {'admin_state_up': False}}
        port_uuid = self.get_port_uuid(instance_opt, network_opt)
        if not port_uuid:
            return

        port_rst = []
        for i in range(len(port_uuid)):
            port_rst.append(self.neutron.update_port(port_uuid[i], body))

        return port_rst

    def set_port_up(self, instance_opt, network_opt):
        body = {'port': {'admin_state_up': True}}
        port_uuid = self.get_port_uuid(instance_opt, network_opt)
        if not port_uuid:
            return

        port_rst = []
        for i in range(len(port_uuid)):
            port_rst.append(self.neutron.update_port(port_uuid[i], body))

        return port_rst

    def set_network_down(self, network_opt):
        network_uuid = self.get_network_uuid(network_opt)
        if not network_uuid:
            return
        body = {'network': {'admin_state_up': False}}

        network_rst = self.neutron.update_network(network_uuid, body)
        return network_rst

    def set_network_up(self, network_opt):
        network_uuid = self.get_network_uuid(network_opt)
        if not network_uuid:
            return
        body = {'network': {'admin_state_up': True}}

        network_rst = self.neutron.update_network(network_uuid, body)
        return network_rst

    def test_method(self):
        Reporter.unit_test_start()
