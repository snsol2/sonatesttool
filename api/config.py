# Copyright 2016 Telcoware

from oslo_config import cfg


CONF = cfg.CONF

default_group = cfg.OptGroup(name='DEFAULT')

default_conf = [
    cfg.IntOpt('network_cnt'),
]

CONF.register_group(default_group)
CONF.register_opts(default_conf, default_group)


class ReadConfig:
    def __init__(self, conf_file):
        CONF(default_config_files=[conf_file])

    @classmethod
    def get_auth_conf(cls):
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

    @classmethod
    def get_network_conf(cls):

        print CONF.DEFAULT.network_cnt

        network_group1 = cfg.OptGroup(name='network1')

        network_group2 = cfg.OptGroup(name='network2')

        network_group3 = cfg.OptGroup(name='network3')

        network_conf1 = [
            cfg.StrOpt('network'),
            cfg.StrOpt('subnet')
        ]

        network_conf2 = [
            cfg.StrOpt('network'),
            cfg.StrOpt('subnet')
        ]

        network_conf3 = [
            cfg.StrOpt('network'),
            cfg.StrOpt('subnet')
        ]

        CONF.register_group(network_group1)
        CONF.register_opts(network_conf1, network_group1)

        CONF.register_group(network_group2)
        CONF.register_opts(network_conf2, network_group2)

        CONF.register_group(network_group3)
        CONF.register_opts(network_conf3, network_group3)

        return CONF.network1, CONF.network2, CONF.network3

