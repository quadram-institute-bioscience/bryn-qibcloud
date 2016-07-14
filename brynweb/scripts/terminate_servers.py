
from openstack.client import OpenstackClient
from openstack.models import Tenant
from userdb.models import Team, Region
import sys
import yaml
import pprint

def delete_instances(tenant):
    client = OpenstackClient(tenant.region.name,
                             username=tenant.get_auth_username(),
                             password=tenant.auth_password,
                             project_name=tenant.get_tenant_name())

    nova = client.get_nova()

    servers = []
    for s in nova.servers.list(detailed=True):
        print s.name
        s.delete()

    return servers

def run():
    for team in Team.objects.filter():
        if team.pk >= 16 and team.pk <= 25:
            tenant = Tenant.objects.filter(team=team, region=Region.objects.get(name='warwick'))[0]
            delete_instances(tenant)
 
