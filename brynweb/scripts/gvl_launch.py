
from openstack.client import OpenstackClient
from openstack.models import Tenant
from userdb.models import Team, Region
from openstack.utils import add_keypair, add_floating_ip

import sys
import yaml
import time

def launch_gvl(tenant, server_name, password, server_type='group'):
    client = OpenstackClient(tenant.region.name,
                             username=tenant.get_auth_username(),
                             password=tenant.auth_password,
                             project_name=tenant.get_tenant_name())

    nova = client.get_nova()

    key_name = add_keypair(nova, 'cloudman', """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDHJwmiJh8wKtl9zYty/eN6+zmBUrObDfdk4HfvWYU/+G8sGrjzd8IBikEDWXMTfp40ZG8OsHacTxBODzPWFAGl5TE5FT89OQ7rbQa1nsYsZqBsy+k0IaVU0EzNQUvkWrLD2SO2hYV9NzwByjLZ3cIl2lndpd7xTlOTLef8RbmPkks9nIW5DDvtG5Ac/bh8e5gJaTvNfNHO2KAoNlYkCya1FS2WqnuQ1CzdEiQb4VWUdW7ix8obs4v42W38HnTN4CjlkCcAdGyaeAQlogxed3/S++nlYn/Memedx+cIzDqyf8+2N7RFMgU3j91nVXy2CPMRJlhkGjxmpS2CthUVew1d cloudman@cloudman""")

    #server_name = "%s-%s" % (tenant.team.name, server_type)

    user_specific_data = {'cloud_name'   : 'CLIMB',
                          'cluster_name' : server_name,
                          'key_name'     : key_name,
                          'password'     : password,
                          'freenxpass'   : password}

    tenant_id = tenant.created_tenant_id
    access, secret = client.get_ec2_keys(tenant_id)

    user_specific_data['access_key'] = access
    user_specific_data['secret_key'] = secret

    cloud_specific_data = {'ec2_conn_path'   : '/services/Cloud'}

    cloud_specific_data['cidr_range'] = client.get_cidr_range()
    cloud_specific_data['ec2_port'] = client.get_ec2_port()
    cloud_specific_data['is_secure'] = client.get_ec2_is_secure()
    cloud_specific_data['region_endpoint'] = client.get_ec2_region_endpoint()

    generic_data = """cloud_type: openstack
region_name: nova
default_bucket_url: https://gvl-filesystem.s3.climb.ac.uk/
use_object_store: false
initial_cluster_type: Galaxy
galaxy_data_option: transient
gvl_config:
  install:
  - gvl_cmdline_utilities
post_start_script_url: 'file:///mnt/galaxy/gvl/poststart.d'
cluster_templates:
  - name: Galaxy
    filesystem_templates:
    - name: galaxy
      type: transient
      roles: galaxyTools,galaxyData
      data_source: archive
      archive_url: https://gvl-filesystem.s3.climb.ac.uk/gvl-galaxyfs-4.2.0.tar.gz
      archive_md5: bc98a98379f70a5c3d81856c1fb27a4f
    - name: gvl
      type: transient
      data_source: archive
      archive_url: https://gvl-filesystem.s3.climb.ac.uk/gvl-apps-4.2-3.tar.gz
      archive_md5: 84045e4f0b8cd15d807beefd1c6aefca
    - name: galaxyIndices
      type: transient
      roles: galaxyIndices
      archive_url: https://gvl-filesystem.s3.climb.ac.uk/gvl-indices-blank-4.2.0.tar.gz
      archive_md5: 0c53cc2804031b2d6e713e6ebcd272ba
  - name: Data
    filesystem_templates:
"""

#     archive_url: http://s3.climb.ac.uk/gvl/microgvl-apps-0.11-1-beta.tgz
#     archive_md5: 0c5421da6b4c432625159a9df6e12784
#     archive_url: http://s3.climb.ac.uk/gvl/microgvl-apps-0.11-1-beta-rebuilt.tgz
#     archive_md5: 5c039ffacfe96e875c82c4bc8eb10df1


    userdata = yaml.dump(user_specific_data, default_flow_style=False, allow_unicode=False) + \
                 yaml.dump(cloud_specific_data, default_flow_style=False, allow_unicode=False) + \
                 yaml.dump(yaml.load(generic_data), default_flow_style=False, allow_unicode=False)

    print userdata

    fl = nova.flavors.find(name=server_type)

    cinder = client.get_cinder()

    volume = cinder.volumes.create(imageRef=tenant.region.regionsettings.gvl_image_id,
                                       name="%s %s boot volume" % (tenant.get_tenant_name(), server_name,),
                                       size=120)
    cinder.volumes.set_bootable(volume, True)

    print volume.id
    for n in xrange(30):
        v = cinder.volumes.get(volume.id)
        print v.status
        if v.status == 'available':
            break
        time.sleep(1)


#[{"boot_index": "0", "uuid": "c19be03e-07fb-4d43-8531-c0bc1f8500e6", "volume_size": "120", "source_type": "volume", "destination_type": "volume", "delete_on_termination": false}]

    bdm = [{'uuid' : volume.id, 'source_type' : 'volume', 
           'destination_type' : 'volume',
           'boot_index' : "0",
           'delete_on_termination' : True}]

    server = nova.servers.create(server_name,
           "",
           flavor=fl,
           nics=[{'net-id' : tenant.get_network_id()}],
           userdata=userdata,
           key_name=key_name,
           block_device_mapping_v2=bdm)
    print server

    #time.sleep(3)
    #add_floating_ip(nova, tenant, server)

    return True

def run():
    team = Team.objects.get(pk=1)
    tenant = Tenant.objects.filter(team=team, region=Region.objects.get(name='bham'))[0]
    launch_gvl(tenant, 'test gvl bham', 'testtest99', 'group')
 
