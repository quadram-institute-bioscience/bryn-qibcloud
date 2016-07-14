
from openstack.client import OpenstackClient, get_admin_credentials
from openstack.models import Tenant
from userdb.models import Team, Region
import sys
import yaml
import pprint
import os

def set_quota(tenant):
    client = OpenstackClient(tenant.region.name, **get_admin_credentials(tenant.region.name))
    nova = client.get_nova()
    quota = nova.quotas.get(tenant.created_tenant_id)
    print quota
    nova.quotas.update(tenant.created_tenant_id, cores=128, ram=650000)
    print tenant.created_tenant_id
    cmd = "cinder quota-update --volumes 20 --gigabytes 10000 %s" % (tenant.created_tenant_id)
    os.system(cmd)

def run():
    for team in Team.objects.filter():
        if team.tenants_available:
            tenant = Tenant.objects.filter(team=team, region=Region.objects.get(name='bham'))[0]
            set_quota(tenant)
 
