
from openstack.client import OpenstackClient
from openstack.models import Tenant, get_tenant_for_team
from userdb.models import Team, Region
import sys
import yaml
import pprint

def terminate_test_gvl_servers(tenant):
    client = OpenstackClient(tenant.region.name,
                             username=tenant.get_auth_username(),
                             password=tenant.auth_password,
                             project_name=tenant.get_tenant_name())

    nova = client.get_nova()

    for s in nova.servers.list(detailed=True):
        if s.name == 'Your first GVL server':
            print s
            s.delete()

def run():
    for team in Team.objects.filter():
        tenant = get_tenant_for_team(team, Region.objects.get(name='warwick'))
        if tenant:
            terminate_test_gvl_servers(tenant)
