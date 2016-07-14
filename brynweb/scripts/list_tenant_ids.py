
from openstack.client import OpenstackClient
from openstack.models import Tenant
from userdb.models import Team, Region
import sys
import yaml
import pprint

def run():
    for team in Team.objects.filter():
        if team.tenants_available:
            tenant = Tenant.objects.filter(team=team, region=Region.objects.get(name='warwick'))[0]
            print tenant.created_tenant_id
 
