
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

    servers = []
    for s in nova.servers.list(detailed=True): 
        ip = 'unknown'
        try:
            ip = s.addresses['public'][0]['addr']
        except:
            block = None
            if 'tenant1-private' in s.addresses:
                block = s.addresses['tenant1-private']
            elif 'bryn:tenant-private' in s.addresses:
                block = s.addresses['bryn:tenant-private']
            if block:
                for a in block:
                    if a['OS-EXT-IPS:type'] == 'floating':
                        ip = a['addr']

        try:
            flavor = nova.flavors.get(s.flavor['id']).name
        except:
            flavor = 'unknown'

        servers.append({'id' : s.id,
                        'name' : s.name,
                        'created' : s.created,
                        'flavor' : flavor,
                        'status' : s.status,
                        'ip' : ip})

    return servers

def run():
    team = Team.objects.get(pk=1)
    print team
    tenant = Tenant.objects.filter(team=team, region=Region.objects.get(name='bham'))[0]
    print tenant
    list_instances(tenant)
 
