# Copyright 2016 Telcoware

from oslo_config import cfg


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
        ]

        CONF.register_group(default_group)
        CONF.register_opts(default_conf, default_group)
        CONF(default_config_files=[conf_file])

    @staticmethod
    def get_auth_conf():
        auth_group = cfg.OptGroup(name='auth')

        auth_conf = [
            cfg.StrOpt('username'),
            cfg.StrOpt('password'),
            cfg.StrOpt('tenant_name'),
            cfg.StrOpt('auth_url')
        ]

        CONF.register_group(auth_group)
        CONF.register_opts(auth_conf, auth_group)

        return CONF.auth

    @staticmethod
    def get_network_conf():

        print CONF.DEFAULT.network_cnt

        network_group = cfg.OptGroup(name='network')

        subnet_group = cfg.OptGroup(name='subnet')


        network_conf = [
            cfg.StrOpt('network1'),
            cfg.StrOpt('network2')
        ]

        subnet_conf = [
            cfg.StrOpt('subnet1'),
            cfg.StrOpt('subnet2')
        ]

        CONF.register_group(network_group)
        CONF.register_opts(network_conf, network_group)

        CONF.register_group(subnet_group)
        CONF.register_opts(subnet_conf, subnet_group)

        return CONF.network, CONF.subnet

