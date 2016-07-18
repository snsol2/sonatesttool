# Copyright 2016 Telcoware

from oslo_config import cfg



class ReadConfig:
    def __init__(self, conf_file):
        self.CONF = cfg.CONF
        default_group = cfg.OptGroup(name='DEFAULT')
        default_conf = [
            cfg.IntOpt('network_cnt'),
            cfg.IntOpt('subnet_cnt'),
            cfg.IntOpt('instance_cnt'),
            cfg.IntOpt('securitygroup_cnt'),
            cfg.IntOpt('rule_cnt'),
            cfg.IntOpt('router_cnt'),
            cfg.IntOpt('floatingip_cnt'),
            cfg.StrOpt('report_path'),
            cfg.StrOpt('test_mode')
        ]
        self.CONF.register_group(default_group)
        self.CONF.register_opts(default_conf, default_group)
        self.CONF(default_config_files=[conf_file])
        # self.config_file = conf_file

    def get_file_path(self):
        return self.CONF.DEFAULT.report_path

    def get_test_mode(self):
        return self.CONF.DEFAULT.test_mode

    def get_openstack_info(self):
        tail_info_group = cfg.OptGroup(name='openstack')
        tail_info_conf = [
            cfg.StrOpt('os_username'),
            cfg.StrOpt('os_password'),
            cfg.StrOpt('controller_ip'),
            cfg.StrOpt('log_files')
        ]
        self.CONF.register_group(tail_info_group)
        self.CONF.register_opts(tail_info_conf, tail_info_group)
        return self.CONF.openstack

    def get_onos_info(self):
        onos_info_group = cfg.OptGroup(name='onos')
        onos_info_conf = [
            cfg.StrOpt('user_id'),
            cfg.StrOpt('password'),
            cfg.StrOpt('ssh_port'),
            cfg.StrOpt('os_username'),
            cfg.StrOpt('os_password'),
            cfg.StrOpt('onos_logfile'),
            cfg.StrOpt('onos_list')
        ]
        self.CONF.register_group(onos_info_group)
        self.CONF.register_opts(onos_info_conf, onos_info_group)
        self.CONF.onos.onos_list = self.CONF.onos.onos_list.split(', ')
        return self.CONF.onos

    def get_auth_conf(self):
        auth_group = cfg.OptGroup(name='auth')
        auth_conf = [
            cfg.StrOpt('version'),
            cfg.StrOpt('username'),
            cfg.StrOpt('api_key'),
            cfg.StrOpt('project_id'),
            cfg.StrOpt('auth_url')
        ]
        self.CONF.register_group(auth_group)
        self.CONF.register_opts(auth_conf, auth_group)
        return self.CONF.auth

    def get_network_config(self):
        network_group = cfg.OptGroup(name='network')

        network_conf = list()
        for i in range(1, self.CONF.DEFAULT.network_cnt + 1):
            network_name = ('network' + str(i))
            network_conf.append(cfg.StrOpt(network_name))

        self.CONF.register_group(network_group)
        self.CONF.register_opts(network_conf, network_group)

        return self.CONF.network

    def get_subnet_config(self):
        subnet_group = cfg.OptGroup(name='subnet')

        subnet_conf = list()
        for i in range(1, self.CONF.DEFAULT.subnet_cnt + 1):
            subnet_name = ('subnet' + str(i))
            subnet_conf.append(cfg.StrOpt(subnet_name))

        self.CONF.register_group(subnet_group)
        self.CONF.register_opts(subnet_conf, subnet_group)

        return self.CONF.subnet

    def get_instance_config(self):
        instance_group = cfg.OptGroup(name='instance')

        instance_conf = list()
        for i in range(1, self.CONF.DEFAULT.instance_cnt + 1):
            instance_name = ('instance' + str(i))
            instance_conf.append(cfg.StrOpt(instance_name))

        self.CONF.register_group(instance_group)
        self.CONF.register_opts(instance_conf, instance_group)

        return self.CONF.instance

    def get_sg_config(self):
        sg_group = cfg.OptGroup(name='security_group')

        sg_conf = list()
        for i in range(1, self.CONF.DEFAULT.securitygroup_cnt + 1):
            sg_name = ('sg' + str(i))
            sg_conf.append(cfg.StrOpt(sg_name))

        self.CONF.register_group(sg_group)
        self.CONF.register_opts(sg_conf, sg_group)

        return self.CONF.security_group

    def get_rule_config(self):

        rule_group = cfg.OptGroup(name='security_group_rule')

        rule_conf = list()
        for i in range(1, self.CONF.DEFAULT.rule_cnt + 1):
            rule_name = ('rule' + str(i))
            rule_conf.append(cfg.StrOpt(rule_name))

        self.CONF.register_group(rule_group)
        self.CONF.register_opts(rule_conf, rule_group)

        return self.CONF.security_group_rule

    def get_router_config(self):
        router_group = cfg.OptGroup(name='router')

        router_conf = list()
        for i in range(1, self.CONF.DEFAULT.router_cnt + 1):
            router_name = ('router' + str(i))
            router_conf.append(cfg.StrOpt(router_name))

        self.CONF.register_group(router_group)
        self.CONF.register_opts(router_conf, router_group)

        return self.CONF.router
