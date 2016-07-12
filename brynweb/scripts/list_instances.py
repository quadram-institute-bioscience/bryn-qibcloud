
from openstack.client import OpenstackClient
from openstack.models import Tenant
from userdb.models import Team, Region
import sys
import yaml
import pprint

def list_instances(tenant):
    client = OpenstackClient(tenant.region.name,
                             username=tenant.get_auth_username(),
                             password=tenant.auth_password,
                             project_name=tenant.get_tenant_name())

    nova = client.get_nova()

    for s in nova.servers.list(detailed=True):
        print "%s %s %s %s %s" % (s.name, s.created, nova.flavors.get(s.flavor['id']).name, s.status, s.addresses['public'][0]['addr'])

def run():
    team = Team.objects.get(pk=1)
    print team
    tenant = Tenant.objects.filter(team=team, region=Region.objects.get(name='warwick'))[0]
    print tenant
    list_instances(tenant)
 
