from novaclient import client
from keystoneauth1 import loading
from keystoneauth1 import session
from keystoneclient.v2_0 import client as keystoneclient
from glanceclient import Client

import auth_settings
import sys

class OpenstackClient:
    def __init__(self, region):
        self.region = region
        self.have_sess = False
        self.have_keystone = False
        self.have_nova = False 
        self.have_glance = False
        self.authsettings = auth_settings.AUTHENTICATION[self.region]

    def get_sess(self):
        if not self.have_sess:
            authsettings = auth_settings.AUTHENTICATION[self.region]

            loader = loading.get_plugin_loader('password')
            auth = loader.load_from_options(auth_url=authsettings['AUTH_URL'],
                                           username=authsettings['AUTH_NAME'],
                                           password=authsettings['AUTH_PASSWORD'],
                                           project_name=authsettings['TENANT_NAME'])
            self.sess = session.Session(auth=auth)
            self.have_sess = True
        return self.sess

    def get_nova(self):
        if not self.have_nova:
            sess = self.get_sess()

            self.nova = client.Client(2, session=sess)
        return self.nova

    def get_keystone(self):
        if not self.have_keystone:
            sess = self.get_sess()
            authsettings = auth_settings.AUTHENTICATION[self.region]
            if 'ADMIN_URL' in authsettings:
                self.keystone = keystoneclient.Client(token=sess.get_token(), endpoint=authsettings['ADMIN_URL'])
            else:
                self.keystone = keystoneclient.Client(session=sess)
            self.have_keystone = True
        return self.keystone

    def get_glance(self):
        if not self.have_glance:
            sess = self.get_sess()
            self.glance = Client('2', session=sess)
        return self.glance

    def get_servers(self):
        nova = get_nova(self.region)
        keystone = keystoneclient.Client(session=sess)

        search_opts = { 'all_tenants': True, }

        servers = nova.servers.list(detailed=True, search_opts=search_opts)
        for s in servers:
            print keystone.tenants.get(s.tenant_id)

    #    tenants = {}
    #    for s in servers:
    #        if s.tenant_id not in tenants:
    #            tenants[s.tenant_id] = keystone.tenants.get(s.tenant_id)
    #        s.tenant = tenants[s.tenant_id]

        users = {}
        for s in servers:
            if s.user_id not in users:
                users[s.user_id] = keystone.users.get(s.user_id)
            s.user = users[s.user_id]

        return servers

    def get_ec2_keys(self, tenant_id):
        sess = self.get_sess()
        keystone = self.get_keystone()
        for e in keystone.ec2.list(sess.get_user_id()):
            if e.tenant_id == tenant_id:
                return e.access, e.secret
        e = keystone.ec2.create(sess.get_user_id(), tenant_id)
        return e.access, e.secret

    def get_cidr_range(self):
        return self.authsettings['CIDR']

    def get_ec2_port(self):
        return self.authsettings['EC2_PORT']

    def get_ec2_is_secure(self):
        return self.authsettings['EC2_SECURE']

    def get_ec2_region_endpoint(self):
        return self.authsettings['EC2_ENDPOINT']
