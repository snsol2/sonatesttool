# Copyright 2016 Telcoware
# network control management classes

from novaclient import client
from api.config import ReadConfig
from api.reporter import Reporter
import ast
import time


class InstanceTester:

    def __init__(self, config_file):
        # Get config
        self.auth_conf = ReadConfig(config_file).get_nova_auth_conf()
        self.instance_conf = ReadConfig.get_instance_config()
        self.network_conf = ReadConfig.get_network_config()
        # Get Token and Neutron Object
        self.nova = client.Client(**self.auth_conf)

    def get_instance_lists(self):
        instance_rst = self.nova.servers.list()
        print 'Instance All --->', instance_rst
        return instance_rst

    def get_instance(self, instance_opt):
        try:
            config_value = self.find_instance(instance_opt)
            if config_value:
                instance_rst = self.nova.servers.list(search_opts={'name': config_value['name']})
                if not instance_rst:
                    print 'Not exist openstack --->', instance_opt
                    return
            else:
                print 'Not exist', instance_opt, 'in config --->'
                return

            Reporter.REPORT_MSG("Get Instance  ---> %s %s", instance_opt, instance_rst)
        except:
            Reporter.exception_err_write()

    def create_instance(self, instance_opt, network_opt):
        config_value = self.find_instance(instance_opt)
        image = self.nova.images.find(name=config_value['image'])
        flavor = self.nova.flavors.find(name=config_value['flavor'])

        if not config_value:
            print 'Not exist in config file --->', instance_opt
            return

        # Get openstack network name from network config
        net_name_list = []
        network_opt = network_opt.split(',')
        for a in network_opt:
            net_conf_body = ast.literal_eval(dict(self.network_conf)[a.strip()])
            net_name_list.append(net_conf_body['name'])
            # net_name_list.append(ast.literal_eval(dict(self.network_conf)[a])['network']['name'])

        # Get network uuid from openstack neutron and make nics list
        nics_list = []
        for a in net_name_list:
            nics_list.append({'net-id':  self.nova.networks.find(label=a).id})

        # TODO
        # make sg_list for security_groups name from config file
        sg_list = ['default']

        # create instance
        instance_rst = self.nova.servers.create(name=config_value['name'],
                                                image=image,
                                                flavor=flavor,
                                                availability_zone=config_value['zone'],
                                                nics=nics_list,
                                                security_groups=sg_list)

        if instance_rst:
            time.sleep(5)

        print 'Create Succ --->', instance_rst
        return instance_rst

    def delete_instance(self, instance_opt):
        instance_list = self.get_instance(instance_opt)
        for i in instance_list:
            self.nova.servers.delete(i)
            time.sleep(5)

        print 'Delete Instance --->', instance_opt
        return

    def find_instance(self, instance_opt):
        instance_conf = dict(self.instance_conf)[instance_opt]
        if instance_conf:
            # TODO
            # when config file is wrong, exception ...
            config_value = ast.literal_eval(instance_conf)
            return config_value
        return None

    #
    # FloatingIP control
    #
    def get_floatingip_list(self):
        floatingip_list = self.nova.floating_ips.list()
        return floatingip_list

    def floatingip_associate(self, instance_opt, pool_opt):
        floatingip_list = self.nova.floating_ips.list()
        server = self.get_instance(instance_opt)
        if not server:
            print 'Floating IP associate Fail --->'
            return
        extra_floatingip = ''

        for a in floatingip_list:
            if not a.fixed_ip:
                extra_floatingip = a.ip
                break

        if not extra_floatingip:
            extra_floatingip = self.nova.floating_ips.create(pool=pool_opt).ip

        # TODO
        # add fixed-ip option
        print server[0], extra_floatingip
        self.nova.servers.add_floating_ip(server[0], extra_floatingip)

        print 'Floating IP Associate --->', self.nova.floating_ips.list()

    def floatingip_separate(self, instance_opt):
        floatingip_list = self.get_floatingip_list()
        instance_list = self.get_instance(instance_opt)
        for i in instance_list:
            for f in floatingip_list:
                if i.id == f.instance_id:
                    self.nova.servers.remove_floating_ip(i, f.ip)
        return

    def delete_floatingip_all(self):
        floatingip_list = self.get_floatingip_list()
        for f in floatingip_list:
            self.nova.floating_ips.delete(f)
        return

