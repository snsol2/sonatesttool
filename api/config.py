# Copyright 2016 Telcoware

from oslo_config import cfg
import ast


CONF = cfg.CONF

# default_group = cfg.OptGroup(name='DEFAULT')
#
# default_conf = [
#     cfg.IntOpt('network_cnt'),
# ]
#
# CONF.register_group(default_group)
# CONF.register_opts(default_conf, default_group)


class ReadConfig:
    def __init__(self, conf_file):
        default_group = cfg.OptGroup(name='DEFAULT')
        default_conf = [
            cfg.IntOpt('network_cnt'),
            cfg.IntOpt('subnet_cnt')
        ]
        CONF.register_group(default_group)
        CONF.register_opts(default_conf, default_group)
        CONF(default_config_files=[conf_file])

    @classmethod
    def get_net_auth_conf(cls):
        auth_group = cfg.OptGroup(name='net_auth')
        auth_conf = [
            cfg.StrOpt('username'),
            cfg.StrOpt('password'),
            cfg.StrOpt('tenant_name'),
            cfg.StrOpt('version'),
            cfg.StrOpt('auth_url')
        ]
        CONF.register_group(auth_group)
        CONF.register_opts(auth_conf, auth_group)
        return CONF.net_auth

    @classmethod
    def get_nova_auth_conf(cls):
        auth_group = cfg.OptGroup(name='nova_auth')
        auth_conf = [
            cfg.StrOpt('version'),
            cfg.StrOpt('username'),
            cfg.StrOpt('api_key'),
            cfg.StrOpt('project_id'),
            cfg.StrOpt('auth_url')
        ]
        CONF.register_group(auth_group)
        CONF.register_opts(auth_conf, auth_group)
        return CONF.nova_auth

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
        for i in range(1, CONF.DEFAULT.network_cnt + 1):
            subnet_name = ('subnet' + str(i))
            subnet_conf.append(cfg.StrOpt(subnet_name))

        CONF.register_group(subnet_group)
        CONF.register_opts(subnet_conf, subnet_group)

        return CONF.subnet

    # Move to network module
    # @classmethod
    # def get_openstack_network_name(cls, network_opt_name):
    #     network_conf = cls.get_network_config()[network_opt_name]
    #     openstack_network_name = ast.literal_eval(network_conf)['network']['name']
    #     return openstack_network_name

