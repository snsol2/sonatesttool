# Copyright 2016 Telcoware

from oslo_config import cfg

CONF = cfg.CONF


class ReadConfig:
    def __init__(self, conf_file):
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
            cfg.StrOpt('report_format'),
            cfg.StrOpt('test_mode'),
            cfg.IntOpt('log_collector_wait_time'),
            cfg.IntOpt('ssh_conn_timeout'),
            cfg.IntOpt('onos_get_timeout'),
            cfg.IntOpt('floating_ip_check_timeout')
        ]
        CONF.register_group(default_group)
        CONF.register_opts(default_conf, default_group)
        CONF(default_config_files=[conf_file])
        self.config_file = conf_file

    @classmethod
    def get_log_collector_wait_time(cls):
        return CONF.DEFAULT.log_collector_wait_time

    @classmethod
    def get_ssh_conn_timeout(cls):
        return CONF.DEFAULT.ssh_conn_timeout

    @classmethod
    def get_onos_timeout(cls):
        return CONF.DEFAULT.onos_get_timeout

    @classmethod
    def get_report_file_path(cls):
        return CONF.DEFAULT.report_path

    @classmethod
    def get_report_file_format(cls):
        return CONF.DEFAULT.report_format

    @classmethod
    def get_floating_ip_check_timeout(cls):
        return CONF.DEFAULT.floating_ip_check_timeout

    @classmethod
    def get_test_mode(cls):
        return CONF.DEFAULT.test_mode

    @classmethod
    def get_openstack_info(cls):
        tail_info_group = cfg.OptGroup(name='openstack')
        tail_info_conf = [
            cfg.StrOpt('os_username'),
            cfg.StrOpt('os_password'),
            cfg.StrOpt('controller_ip'),
            cfg.StrOpt('log_files'),
            cfg.BoolOpt('log_collector')
        ]
        CONF.register_group(tail_info_group)
        CONF.register_opts(tail_info_conf, tail_info_group)
        CONF.openstack.log_files = CONF.openstack.log_files.split(', ')
        return CONF.openstack

    @classmethod
    def get_onos_info(cls):
        onos_info_group = cfg.OptGroup(name='onos')
        onos_info_conf = [
            cfg.StrOpt('user_id'),
            cfg.StrOpt('password'),
            cfg.StrOpt('ssh_port'),
            cfg.StrOpt('os_username'),
            cfg.StrOpt('os_password'),
            cfg.StrOpt('onos_logfile'),
            cfg.StrOpt('onos_list'),
            cfg.BoolOpt('log_collector')
        ]
        CONF.register_group(onos_info_group)
        CONF.register_opts(onos_info_conf, onos_info_group)
        CONF.onos.onos_list = CONF.onos.onos_list.split(', ')
        CONF.onos.onos_logfile = CONF.onos.onos_logfile.split(', ')
        return CONF.onos

    @classmethod
    def get_auth_conf(cls):
        auth_group = cfg.OptGroup(name='openstack')
        auth_conf = [
            cfg.StrOpt('version'),
            cfg.StrOpt('username'),
            cfg.StrOpt('api_key'),
            cfg.StrOpt('project_id'),
            cfg.StrOpt('auth_url')
        ]
        CONF.register_group(auth_group)
        CONF.register_opts(auth_conf, auth_group)
        return CONF.openstack

    @classmethod
    def get_network_config(cls):

        network_group = cfg.OptGroup(name='network')

        network_conf = list()
        for i in range(1, CONF.DEFAULT.network_cnt + 1):
            network_name = ('network' + str(i))
            network_conf.append(cfg.StrOpt(network_name))

        CONF.register_group(network_group)
        CONF.register_opts(network_conf, network_group)

        return CONF.network

    @classmethod
    def get_subnet_config(cls):

        subnet_group = cfg.OptGroup(name='subnet')

        subnet_conf = list()
        for i in range(1, CONF.DEFAULT.subnet_cnt + 1):
            subnet_name = ('subnet' + str(i))
            subnet_conf.append(cfg.StrOpt(subnet_name))

        CONF.register_group(subnet_group)
        CONF.register_opts(subnet_conf, subnet_group)

        return CONF.subnet

    @classmethod
    def get_instance_config(cls):

        instance_group = cfg.OptGroup(name='instance')

        instance_conf = list()
        for i in range(1, CONF.DEFAULT.instance_cnt + 1):
            instance_name = ('instance' + str(i))
            instance_conf.append(cfg.StrOpt(instance_name))

        CONF.register_group(instance_group)
        CONF.register_opts(instance_conf, instance_group)

        return CONF.instance

    @classmethod
    def get_sg_config(cls):

        sg_group = cfg.OptGroup(name='security_group')

        sg_conf = list()
        for i in range(1, CONF.DEFAULT.securitygroup_cnt + 1):
            sg_name = ('sg' + str(i))
            sg_conf.append(cfg.StrOpt(sg_name))

        CONF.register_group(sg_group)
        CONF.register_opts(sg_conf, sg_group)

        return CONF.security_group

    @classmethod
    def get_rule_config(cls):

        rule_group = cfg.OptGroup(name='security_group_rule')

        rule_conf = list()
        for i in range(1, CONF.DEFAULT.rule_cnt + 1):
            rule_name = ('rule' + str(i))
            rule_conf.append(cfg.StrOpt(rule_name))

        CONF.register_group(rule_group)
        CONF.register_opts(rule_conf, rule_group)

        return CONF.security_group_rule

    @classmethod
    def get_router_config(cls):

        router_group = cfg.OptGroup(name='router')

        router_conf = list()
        for i in range(1, CONF.DEFAULT.router_cnt + 1):
            router_name = ('router' + str(i))
            router_conf.append(cfg.StrOpt(router_name))

        CONF.register_group(router_group)
        CONF.register_opts(router_conf, router_group)

        return CONF.router

