# Copyright 2017 Telcoware
# identity control management classes

from keystoneauth1.identity import v2
from keystoneauth1 import session
from keystoneclient.v2_0 import client
from keystoneclient import exceptions

from api.config import ReadConfig
from api.reporter2 import Reporter


class Identity:
    def __init__(self, config):
        self.identity = config.get_identity()
        self.openstack_admin = config.get_auth_conf()
        self.admin_user = self.get_admin_auth(self.openstack_admin)

    def get_admin_auth(self, user):
        try:
            auth = v2.Password(username=user['username'],
                               password=user['api_key'],
                               tenant_name=user['project_id'],
                               auth_url=user['auth_url'])
            sess = session.Session(auth=auth, timeout=5)
            return client.Client(session=sess)
            # return sess
        except:
            Reporter.exception_err_write()

    def create_user(self):
        Reporter.unit_test_start(True)
        tenant_id = ''
        user_id = ''
        try:
            tenant_id = self.admin_user.tenants.create(tenant_name=self.identity['tenant_id'],
                                                     description="SONA Test Temporary Tenant",
                                                     enabled=True).id
        except exceptions.Conflict, err:
            tenant_list = self.admin_user.tenants.list()
            tenant_id = [x.id for x in tenant_list if x.name == self.identity['tenant_id']][0]
            Reporter.REPORT_MSG("   >> Already exist tenant(%s) > tenant_id: %s",
                                self.identity['tenant_id'], tenant_id)
        except:
            Reporter.exception_err_write()

        # Reporter.NRET_PRINT("aaa %s\n", tenant_id)
        try:
            user_id = self.admin_user.users.create(name=self.identity['username'],
                                                    password=self.identity['password'],
                                                    tenant_id=tenant_id).id

            admin_role_id = [x.id for x in self.admin_user.roles.list() if x.name == 'admin'][0]
            self.admin_user.roles.add_user_role(user_id, admin_role_id, tenant_id)

        except exceptions.Conflict, err:
            user_list = self.admin_user.users.list()
            user_id = [x.id for x in user_list if x.name == self.identity['username']][0]
            Reporter.REPORT_MSG("   >> Already exist User(%s) > user_id: %s",
                                self.identity['username'], user_id)
            Reporter.unit_test_stop('skip')
            return
        except:
            Reporter.exception_err_write()

        if user_id:
            Reporter.REPORT_MSG("   >> Create User(%s) > user_id: %s",
                                self.identity['username'], user_id)
            Reporter.unit_test_stop('ok')
        else:
            Reporter.REPORT_MSG("   >> Create User(%s) fail > ", self.identity['username'])
            Reporter.unit_test_stop('nok')

    def delete_user(self):
        Reporter.unit_test_start(True)
        try:
            user_list = self.admin_user.users.list()
            user_id = [x.id for x in user_list if x.name == self.identity['username']][0]
            if not user_id:
                Reporter.REPORT_MSG("   >> User(%s) Not Exist > ", self.identity['username'])
                Reporter.unit_test_stop('skip')
            else:
                self.admin_user.users.delete(user_id)
                Reporter.REPORT_MSG("   >> User(%s) Delete OK > ", self.identity['username'])

            tenant_list = self.admin_user.tenants.list()
            tenant_id = [x.id for x in tenant_list if x.name == self.identity['tenant_id']][0]
            if not tenant_id:
                Reporter.REPORT_MSG("   >> Tenent(%s) Not Exist > ", self.identity['username'])
                Reporter.unit_test_stop('skip')
            else:
                self.admin_user.tenants.delete(tenant_id)
                Reporter.REPORT_MSG("   >> Tenant(%s) Delete OK > ", self.identity['tenant_id'])

            if user_id and tenant_id:
                Reporter.unit_test_stop('ok')

        except:
            Reporter.exception_err_write()

