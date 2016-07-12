
from django.contrib.auth.models import User
from userdb.models import Team, Region
from openstack.client import OpenstackClient
from openstack.models import Tenant

def setup_tenant(team, region):
    client = OpenstackClient(region.name)
    nova = client.get_nova()
    keystone = client.get_keystone()

    tenant = Tenant(team=team, region=region)

    tenant_name = tenant.get_tenant_name()
    tenant_description = tenant.get_tenant_description()

    openstack_tenant = keystone.tenants.create(
        tenant_name=tenant_name,   
        description=tenant_description,
        enabled=True)

    username = tenant.get_auth_username()
    password = User.objects.make_random_password(length=16)

    user = keystone.users.create(
        name=username,
        password=password,
        tenant_id=openstack_tenant.id)

    tenant.created_tenant_id = openstack_tenant.id
    tenant.auth_password = password

    tenant.save()

def run():
    t = Team.objects.get(name='Loman Labz')
    setup_tenant(t, Region.objects.get(name='bham'))
