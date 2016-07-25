# Copyright 2016 Telcoware
# network control management classes

from novaclient import client
# from api.config import ReadConfig
from api.reporter2 import Reporter
import ast


class InstanceTester:

    # def __init__(self, config_file):
    def __init__(self, config):
        # Get config
        self.auth_conf = config.get_auth_conf()
        self.instance_conf = config.get_instance_config()
        self.network_conf = config.get_network_config()
        self.sg_config = config.get_sg_config()
        # Get Token and Neutron Object
        self.nova = client.Client(**self.auth_conf)

    def get_instance_lists(self):
        instance_rst = self.nova.servers.list()
        print ' >> GET Instance All --->', instance_rst
        return instance_rst

    def get_instance(self, instance_opt):
        config_value = self.find_instance(instance_opt)
        if not config_value:
            return

        instance_rst = self.nova.servers.list(search_opts={'name': config_value['name']})
        if not instance_rst:
            Reporter.REPORT_MSG("   >> Not exist openstack ---> %s", instance_opt)
            return

        Reporter.REPORT_MSG("   >> Get Instance  ---> %s %s", instance_opt, instance_rst)
        return instance_rst

    def find_instance(self, instance_opt):
        instance_conf = dict(self.instance_conf)[instance_opt]
        if not instance_conf:
            Reporter.REPORT_MSG("   >> Not exist in config ---> %s", instance_opt)
            return

        config_value = ast.literal_eval(instance_conf)
        return config_value

    def create_instance(self, instance_opt, network_opt, sg_opt):
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

            if sg_opt is '':
                sg_list = ['default']
            else:
                sg_list = [ast.literal_eval(dict(self.sg_config)[sg_opt])['name']]

            # create instance
            instance_rst = self.nova.servers.create(name=config_value['name'],
                                                    image=image,
                                                    flavor=flavor,
                                                    availability_zone=config_value['zone'],
                                                    nics=nics_list,
                                                    security_groups=sg_list)

            Reporter.REPORT_MSG("   >> Create Succ ---> %s", instance_rst)
            Reporter.unit_test_stop('ok')
            return instance_rst
        except:
            Reporter.exception_err_write()

    def delete_instance(self, instance_opt):
        Reporter.unit_test_start()
        try:
            instance_list = self.get_instance(instance_opt)
            if not instance_list:
                Reporter.unit_test_stop('skip')
                return
            for i in instance_list:
                self.nova.servers.delete(i)
                # time.sleep(5)

            Reporter.REPORT_MSG("   >> Delete Instance ---> %s", instance_opt)
            Reporter.unit_test_stop('ok')
            return
        except:
            Reporter.exception_err_write()

    #
    # FloatingIP control
    #
    def get_floatingip_list(self):
        floatingip_list = self.nova.floating_ips.list()
        return floatingip_list

    def floatingip_associate(self, instance_opt, network_opt):
        Reporter.unit_test_start()
        try:
            server = self.get_instance(instance_opt)
            if not server:
                Reporter.unit_test_stop('nok')
                return

            floatingip_list = self.nova.floating_ips.list()
            if not floatingip_list:
                Reporter.REPORT_MSG("   >> Not exist floating IPs --->")

            extra_floatingip = ''
            for a in floatingip_list:
                if not a.fixed_ip:
                    extra_floatingip = a.ip
                    break

            pool_opt = ast.literal_eval(dict(self.network_conf)[network_opt])['name']

            if not extra_floatingip:
                extra_floatingip = self.nova.floating_ips.create(pool=pool_opt).ip

            # TODO
            # add fixed_address option
            self.nova.servers.add_floating_ip(server[0],
                                              extra_floatingip,
                                              fixed_address=None)
            Reporter.REPORT_MSG("   >> Floating IP Associate ---> %s",
                                self.nova.floating_ips.list())
            Reporter.unit_test_stop('ok')
        except:
            Reporter.exception_err_write()

    def floatingip_separate(self, instance_opt):
        floatingip_list = self.get_floatingip_list()
        instance_list = self.get_instance(instance_opt)
        for i in instance_list:
            for f in floatingip_list:
                if i.id == f.instance_id:
                    self.nova.servers.remove_floating_ip(i, f.ip)
        return

    def delete_floatingip_all(self):
        Reporter.unit_test_start()
        try:
            floatingip_list = self.get_floatingip_list()
            if not floatingip_list:
                Reporter.REPORT_MSG("   >> Not exist Floating IP --->")
                Reporter.unit_test_stop('skip')
                return
            for f in floatingip_list:
                self.nova.floating_ips.delete(f)
            Reporter.REPORT_MSG("   >> All Floating IP Delete Succ --->")
            Reporter.unit_test_stop('ok')
            return
        except:
            Reporter.exception_err_write()

    def get_instance_floatingip(self, instance_opt):
        instance_rst = self.get_instance(instance_opt)
        if not instance_rst:
            return
        instance_uuid = instance_rst[0].id

        floatingip_list = self.get_floatingip_list()
        if not floatingip_list:
            return

        floatingip = ''
        for i in range(len(floatingip_list)):
            if instance_uuid == floatingip_list[i].instance_id:
                floatingip = floatingip_list[i].ip
        if not floatingip:
            return
        return floatingip

    def get_instance_ip(self, instance_network):
        instance_opt, network_opt = instance_network.split(':')
        instance_rst = self.get_instance(instance_opt)[0].__dict__
        network_cfg_body = self.network_conf[network_opt]
        if not (instance_rst and network_cfg_body):
            return

        network_name = ast.literal_eval(network_cfg_body)['name']

        instance_ip = instance_rst['addresses'][network_name][0]['addr']
        if not instance_ip:
            return
        return instance_ip
