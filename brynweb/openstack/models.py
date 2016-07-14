from __future__ import unicode_literals

from django.db.models import *
from userdb.models import Team, Region
from openstack.client import OpenstackClient
import uuid

class Tenant(Model):
    team = ForeignKey(Team)
    region = ForeignKey(Region)
    created_tenant_id = CharField(max_length=50)
    auth_password = CharField(max_length=50)
    created_network_id = CharField(max_length=50)

    def get_tenant_name(self):
        return "bryn:%d_%s" % (self.team.pk, self.team.name)

    def get_tenant_description(self):
        return "%s (%s)" % (self.team.name, self.team.creator.last_name)

    def get_client(self):
        client = OpenstackClient(self.region.name,
                                 username=self.get_auth_username(),
                                 password=self.auth_password,
                                 project_name=self.get_tenant_name())
        return client

    def get_server(self, uuid):
        client = self.get_client()
        nova = client.get_nova()
        return nova.servers.get(uuid)

    def get_images(self):
        client = self.get_client()
        glance = client.get_glance()

        return [(i.id, i.name) for i in glance.images.list()]

    def get_keys(self):
        client = self.get_client()
        nova = client.get_nova()
        return [(k.name, k.name) for k in nova.keypairs.list()]

    def get_auth_username(self):
        return self.get_tenant_name()

    def start_server(self, uuid):
        server = self.get_server(uuid)
        server.start()

    def stop_server(self, uuid):
        server = self.get_server(uuid)
        server.stop()

    def terminate_server(self, uuid):
        server = self.get_server(uuid)
        server.delete()

    def reboot_server(self, uuid):
        server = self.get_server(uuid)
        server.reboot(reboot_type='HARD') 

    def __str__(self):
        return "%s - %s" % (self.get_tenant_name(), self.region)

class RegionSettings(Model):
    region = OneToOneField(Region)
    gvl_image_id = CharField(max_length=50)
    public_network_id = CharField(max_length=50)
    requires_network_setup = BooleanField(default=False)

    def __str__(self):
        return str(self.region)

def get_tenant_for_team(team, region):
    tenant = Tenant.objects.filter(team=team, region=Region.objects.get(name=region))
    if not tenant:
        return None
    if len(tenant) > 1:
        return None
    return tenant[0]
