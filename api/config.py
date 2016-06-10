# Copyright 2016 Telcoware

from oslo_config import cfg

auth_group = cfg.OptGroup(name='auth',
                         title='A Simple Example')

AuthGroup = [
    cfg.StrOpt('username'),
    cfg.StrOpt('password'),
    cfg.StrOpt('tenant_name', default='admin', ),
    cfg.StrOpt('auth_url', default='http://controller:5000/v2.0', )
]

CONF = cfg.CONF
CONF.register_group(auth_group)
CONF.register_opts(AuthGroup, auth_group)


class ReadConfig:
    def __init__(self, conf_file):
        CONF(default_config_files=[conf_file])

    def get_auth_conf(self):
        return CONF.auth

