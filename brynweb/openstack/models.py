from __future__ import unicode_literals

from django.db.models import *
from userdb.models import Team, Region
import uuid

class Tenant(Model):
    team = ForeignKey(Team)
    region = ForeignKey(Region)
    created_tenant_id = CharField(max_length=50)
    auth_password = CharField(max_length=50)

    def get_tenant_name(self):
        return "bryn:%d_%s" % (self.team.pk, self.team.name)

    def get_tenant_description(self):
        return "%s (%s)" % (self.team.name, self.team.creator.last_name)

    def get_auth_username(self):
        return self.get_tenant_name()

    def __str__(self):
        return "%s - %s" % (self.get_tenant_name(), self.region)

class RegionSettings(Model):
    region = OneToOneField(Region)
    gvl_image_id = CharField(max_length=50)

    def __str__(self):
        return str(self.region)

def get_tenant_for_team(team, region):
    tenant = Tenant.objects.filter(team=team, region=Region.objects.get(name='warwick'))
    if not tenant:
        return None
    if len(tenant) > 1:
        return None
    return tenant[0]
