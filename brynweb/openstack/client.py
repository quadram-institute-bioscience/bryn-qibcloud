from novaclient import client
from keystoneauth1 import loading
from keystoneauth1 import session
from keystoneclient.v2_0 import client as keystoneclient
import auth_settings
import sys

def get_sess(region):
    authsettings = auth_settings.AUTHENTICATION[region]

    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(auth_url=authsettings['AUTH_URL'],
                                   username=authsettings['AUTH_NAME'],
                                   password=authsettings['AUTH_PASSWORD'],
                                   project_name=authsettings['TENANT_NAME'])
    sess = session.Session(auth=auth)
    return sess

def get_nova(region):
    sess = get_sess(region) 

    return client.Client(2, session=sess)

def get_servers(region):
    nova = get_nova(region)
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

