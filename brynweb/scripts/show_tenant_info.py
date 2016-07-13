
from django.contrib.auth.models import User
from userdb.models import Team, Region
from openstack.client import OpenstackClient, get_admin_credentials
from openstack.models import Tenant

def show_tenant_info(tenant):
    client = OpenstackClient(tenant.region.name, **get_admin_credentials(tenant.region.name))
    nova = client.get_nova()
    keystone = client.get_keystone()

    user = keystone.users.list()
    for u in user:
        if u.name == tenant.get_auth_username():
            print u

    t = keystone.tenants.get(tenant.created_tenant_id)
    print t

    print tenant.auth_password

def run():
    t = Team.objects.get(name='Loman Labz')
    tenant = Tenant.objects.filter(team=t, region=Region.objects.get(name='warwick'))[0]
    show_tenant_info(tenant)
