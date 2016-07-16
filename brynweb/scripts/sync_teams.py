
from django.contrib.auth.models import User
from userdb.models import Team, Region
from openstack.client import OpenstackClient, get_admin_credentials
from openstack.models import Tenant, get_tenant_for_team
from scripts.setup_team import setup_tenant

def run():
    for t in Team.objects.all():
        for r in Region.objects.all():
            tenant = get_tenant_for_team(t, r)
            if not tenant:
                print "%s does not have %s" % (t, r)
                try:
                    setup_tenant(t, r)
                    print "success"
                except Exception, e:
                    print e


