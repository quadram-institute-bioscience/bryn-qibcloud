
from django.contrib.auth.models import User
from userdb.models import Team, Region
from openstack.client import OpenstackClient, get_admin_credentials
from openstack.models import Tenant

def setup_tenant(team, region):
    client = OpenstackClient(region.name, **get_admin_credentials(region.name))
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

    ## flip to user tenant
    client = OpenstackClient(region.name,
                             username=tenant.get_auth_username(),
                             password=tenant.auth_password,
                             project_name=tenant.get_tenant_name())
    nova = client.get_nova()

    security_group_name = "bryn:default"

#    group = nova.security_groups.create(
#        security_group_name,
#        'Automatic security group for %s' % (tenant_name)
#    )
    group = nova.security_groups.find(name="default")

    nova.security_group_rules.create(group.id, ip_protocol="tcp",
                                     from_port=22, to_port=22)
    nova.security_group_rules.create(group.id, ip_protocol="tcp",
                                     from_port=80, to_port=80)
    nova.security_group_rules.create(group.id, ip_protocol="tcp",
                                     from_port=443, to_port=443) 

    tenant.save()

    team.tenants_available = True
    team.save()


def run():
    t = Team.objects.get(name='Loman Labz')
    setup_tenant(t, Region.objects.get(name='warwick'))
