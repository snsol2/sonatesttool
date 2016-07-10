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
        print ' >> GET Instance All --->', instance_rst
        return instance_rst

    def get_instance(self, instance_opt):
        Reporter.unit_test_start()
        try:
            config_value = self.find_instance(instance_opt)
            if not config_value:
                Reporter.unit_test_stop('nok')
                return

            instance_rst = self.nova.servers.list(search_opts={'name': config_value['name']})
            if not instance_rst:
                Reporter.REPORT_MSG("   >> Not exist openstack ---> %s", instance_opt)
                return

            Reporter.REPORT_MSG(" >> Get Instance  ---> %s %s", instance_opt, instance_rst)
            Reporter.unit_test_stop('ok')
            return instance_rst
        except:
            Reporter.exception_err_write()

    def find_instance(self, instance_opt):
        instance_conf = dict(self.instance_conf)[instance_opt]
        if not instance_conf:
            Reporter.REPORT_MSG("   >> Not exist in config ---> %s", instance_opt)
            return

        config_value = ast.literal_eval(instance_conf)
        return config_value

    def create_instance(self, instance_opt, network_opt):
        Reporter.unit_test_start()
        try:
            config_value = self.find_instance(instance_opt)
            if not config_value:
                Reporter.unit_test_stop('nok')
                return

            instance_rst = self.nova.servers.list(search_opts={'name': config_value['name']})
            if instance_rst:
                Reporter.REPORT_MSG("   >> Already exist in OpenStack ---> %s", instance_rst)
                Reporter.unit_test_stop('nok')
                return

            image = self.nova.images.find(name=config_value['image'])
            flavor = self.nova.flavors.find(name=config_value['flavor'])

            # Get openstack network name from network config
            net_name_list = []
            network_opt = network_opt.split(',')
            for a in network_opt:
                net_conf_body = ast.literal_eval(dict(self.network_conf)[a.strip()])
                if not net_conf_body:
                    Reporter.REPORT_MSG("   >> Not exist in config file ---> %s", network_opt)
                    Reporter.unit_test_stop('nok')
                    return
                net_name_list.append(net_conf_body['name'])

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
                                                    # availability_zone=compute_opt,
                                                    nics=nics_list,
                                                    security_groups=sg_list)

            if instance_rst:
                time.sleep(5)

            Reporter.REPORT_MSG("   >> Create Succ ---> %s", instance_rst)
            Reporter.unit_test_stop('ok')
            return instance_rst
        except:
            Reporter.exception_err_write()

    def delete_instance(self, instance_opt):
        instance_list = self.get_instance(instance_opt)
        for i in instance_list:
            self.nova.servers.delete(i)
            time.sleep(5)

        print ' >> Delete Instance --->', instance_opt
        return

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
            print ' >> Floating IP associate Fail --->'
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

        print ' >> Floating IP Associate --->', self.nova.floating_ips.list()

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

    @classmethod
    def instance_test_method(cls):
        Reporter.unit_test_start()
        Reporter.test('nok')
