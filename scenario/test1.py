from novaclient import client as novaclient
from neutronclient.v2_0 import client as neutronclient
import ast

auth_url = "http://controller:5000/v2.0"
username = "admin"
password = "admin"
tenant_name = "admin"
version = 2

nova = novaclient.Client(version=version, auth_url=auth_url, username=username, api_key=password, project_id=tenant_name)

# image = nova.images.find(name='cirros-0.3.4-x86_64')
# flavor = nova.flavors.find(name='m1.tiny')
# net = nova.networks.find(label='test-net')
# sg = nova.security_groups.find(name='default')

server = nova.servers.list(search_opts={'name':'c1vm2'})

# hosts = nova.hosts.list()
aaa = 'dc29116a-7667-4c26-96d9-93d6fe19437f'

# print server[0].id

print nova.servers.get(server[0].id)


print nova.servers.interface_list(aaa)[1].id
# bbb = nova.servers.interface_list(aaa)[1].id
# nova.servers.interface_detach(aaa, bbb)
# print nova.networks.find(label='test-net').
# print 'net-id', net.id
# print sg
#
# nics = [{'net-id': net.id}]
# print nics
# instance = nova.servers.create(name="vm6",
#                                image=image,
#                                flavor=flavor,
#                                nics=nics,
#                                availability_zone=None,
#                                security_groups=None)

# body = 'name=\'vm5\','+' image=image,'+' flavor=flavor,'+' nics=nics,'+' availability_zone=\'compute2\''
# print body
# instance = nova.servers.create(body)

