# Copyright 2016 Telcoware

from oslo_config import cfg

auth_group = cfg.OptGroup(name='auth',
                          title='OpenStack Auth Information')

AuthGroup = [
    cfg.StrOpt('username', default='admin'),
    cfg.StrOpt('password', default='admin'),
    cfg.StrOpt('tenant_name', default='admin'),
    cfg.StrOpt('auth_url', default='http://controller:5000/v2.0', )
]

network_group = cfg.OptGroup(name='network1',
                             title='Network Information')

network_group = cfg.OptGroup(name='network2',
                             title='Network Information')

NetworkGroup = [
    cfg.StrOpt('network', default='admin'),
    cfg.StrOpt('subnet', default='admin'),
]

CONF = cfg.CONF

CONF.register_group(auth_group)
CONF.register_opts(AuthGroup, auth_group)

CONF.register_group(network_group)
CONF.register_opts(NetworkGroup, network_group)


class ReadConfig:
    def __init__(self, conf_file):
        CONF(default_config_files=[conf_file])

    def get_auth_conf(self):
        return CONF.auth

    def get_network_conf(self):
        return CONF.network1, CONF.network2

