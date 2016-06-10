# Copyright 2016 Telcoware


from oslo_config import cfg


opt_group = cfg.OptGroup(name='credentials',
                         title='A Simple Example')

credential_opt = [
    cfg.StrOpt('username', default='admin', ),
    cfg.StrOpt('password', default='admin', ),
    cfg.StrOpt('tenant_name', default='admin', ),
    cfg.StrOpt('auth_url', default='http://controller:5000/v2.0', )
]