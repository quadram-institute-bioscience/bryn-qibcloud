
from django.contrib.auth.models import User
from userdb.models import Team, Region
from openstack.client import OpenstackClient, get_admin_credentials
from openstack.models import Tenant

def delete_tenant(tenant):
    client = OpenstackClient(tenant.region.name, **get_admin_credentials(tenant.region.name))
    nova = client.get_nova()
    keystone = client.get_keystone()

    user = keystone.users.list()
    for u in user:
        if u.name == tenant.get_auth_username():
            print u
            u.delete()

    try:
        t = keystone.tenants.get(tenant.created_tenant_id)
        t.delete()
    except Exception:
        print "Cannot find tenant"

    tenant.delete()

def run():
    tenant = Tenant.objects.filter(region=Region.objects.get(name='cardiff'))
    for t in tenant:
        delete_tenant(tenant)
