
from openstack.client import OpenstackClient
from openstack.models import Tenant
from userdb.models import Team, Region
from openstack.utils import add_floating_ip, add_keypair
import sys
import yaml
import time

def launch_image(tenant, server_name, image_id, auth_key_name, auth_key_value, server_type='group'):
    client = OpenstackClient(tenant.region.name,
                             username=tenant.get_auth_username(),
                             password=tenant.auth_password,
                             project_name=tenant.get_tenant_name())

    nova = client.get_nova()
    key_name = add_keypair(nova, auth_key_name, auth_key_value)

    tenant_id = tenant.created_tenant_id

    fl = nova.flavors.find(name=server_type)
    
    cinder = client.get_cinder()

    volume = cinder.volumes.create(imageRef=image_id,
                                       name="%s %s boot volume" % (tenant.get_tenant_name(), server_name,),
                                       size=120)
    cinder.volumes.set_bootable(volume, True)

    for n in xrange(20):
        v = cinder.volumes.get(volume.id)
        if v.status == 'available':
            break
        time.sleep(1)

    bdm = [{'uuid' : volume.id, 'source_type' : 'volume', 
           'destination_type' : 'volume',
           'boot_index' : "0",
           'delete_on_termination' : True}]

    server = nova.servers.create(server_name,
           "",
           flavor=fl,
           nics=[{'net-id' : tenant.get_network_id()}],
           key_name=key_name,
           block_device_mapping_v2=bdm)

    #time.sleep(3)
    #add_floating_ip(nova, tenant, server)

    return True

def run():
    team = Team.objects.get(pk=1)
    print(team)
    tenant = Tenant.objects.filter(team=team, region=Region.objects.get(name='warwick'))[0]
    print(tenant)
    launch_image(tenant, 'test-ubuntu', '2ae0fe84-74d9-47fe-a744-408ec28026fd', 'launchkey', 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQClUIKUlWckdyjIur2OhEFz4Xa2eKrpZe7ZgcVBnV3eUJi4WCPzB39aD4GvakwsUuKMGno3ipSCBI2Mcw2VfGD9oelCmPA/M6/cDvjijaQSgF5WBNoAbbaARtWyDSu+XMpbftNexmpc3CblamTm3DEgrOnhTcNJ+Imk+wBXpFUZOvfu/Ht/MBldbcgWp2RK8rgX+tCf5GUdgvA3Fz8YyvIOcIHIqSa9c9hfhes2hyLsrxe39norXUgsrgbMWlqqMYLc95TSYRFI+VYstoQ5b/6QHa/UloKkAR8LhVv8ntfRXVgvQtmUh3GzrYu326JW+kYSQ8hMX++v2w84vpL+50Rz nick@Nicks-MacBook-Pro.local', 'group')
 
