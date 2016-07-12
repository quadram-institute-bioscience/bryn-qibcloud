from __future__ import unicode_literals

from django.db.models import *
from userdb.models import Team, Region
import uuid

class Tenant(Model):
    team = ForeignKey(Team)
    region = ForeignKey(Region)
    tenant_name = CharField(max_length=50)
    auth_username = CharField(max_length=50)
    auth_password = CharField(max_length=50)

