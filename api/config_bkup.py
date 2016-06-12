# Copyright 2016 Telcoware

from oslo_config import cfg


CONF = cfg.CONF

auth_group = cfg.OptGroup(name='auth',
                          title='OpenStack Auth Information')

AuthGroup = [
    cfg.StrOpt('username', default='admin'),
    cfg.StrOpt('password', default='admin'),
    cfg.StrOpt('tenant_name', default='admin'),
    cfg.StrOpt('auth_url', default='http://controller:5000/v2.0', )
]

CONF.register_group(auth_group)
CONF.register_opts(AuthGroup, auth_group)


network_group1 = cfg.OptGroup(name='network1',
                             title='Network Information')

network_group2 = cfg.OptGroup(name='network2',
                             title='Network Information')

network_group3 = cfg.OptGroup(name='network3',
                              title='Network Information')

NetworkGroup1 = [
    cfg.StrOpt('network', default='admin1'),
    cfg.StrOpt('subnet', default='admin1')
]

NetworkGroup2 = [
    cfg.StrOpt('network', default='admin1'),
    cfg.StrOpt('subnet', default='admin1')
]

NetworkGroup3 = [
    cfg.StrOpt('network'),
    cfg.StrOpt('subnet')
]


CONF.register_group(network_group1)
CONF.register_opts(NetworkGroup1, network_group1)

CONF.register_group(network_group2)
CONF.register_opts(NetworkGroup2, network_group2)

CONF.register_group(network_group3)
CONF.register_opts(NetworkGroup3, network_group3)


class ReadConfig:
    def __init__(self, conf_file):
        CONF(default_config_files=[conf_file])

    def get_auth_conf(self):
        return CONF.auth

    def get_network_conf(self):
        # return CONF.network1
        return CONF.network1, CONF.network2, CONF.network3

