# from oslo_config import cfg
#
# body_sample = {'network': {'name': 'test', 'admin_state_up': True}}
#
# print body_sample['network']['name']

from api.config import ReadConfig
import ast


# ReadConfig('../config/config.ini').get_openstack_network_name('network1')
conf = ReadConfig('../config/config.ini').get_subnet_config()

print conf.subnet1

subnet_body = ast.literal_eval(conf.subnet1)
subnet_body['subnets'][0]['network'] = 'test'
print subnet_body

