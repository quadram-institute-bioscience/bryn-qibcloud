
from openstack.client import OpenstackClient
from openstack.models import Tenant
from userdb.models import Team, Region
import sys
import yaml
import time

def add_keypair(nova):
    try:
        keypair = nova.keypairs.create(name='default_key', public_key="""ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQClUIKUlWckdyjIur2OhEFz4Xa2eKrpZe7ZgcVBnV3eUJi4WCPzB39aD4GvakwsUuKMGno3ipSCBI2Mcw2VfGD9oelCmPA/M6/cDvjijaQSgF5WBNoAbbaARtWyDSu+XMpbftNexmpc3CblamTm3DEgrOnhTcNJ+Imk+wBXpFUZOvfu/Ht/MBldbcgWp2RK8rgX+tCf5GUdgvA3Fz8YyvIOcIHIqSa9c9hfhes2hyLsrxe39norXUgsrgbMWlqqMYLc95TSYRFI+VYstoQ5b/6QHa/UloKkAR8LhVv8ntfRXVgvQtmUh3GzrYu326JW+kYSQ8hMX++v2w84vpL+50Rz nick@Nicks-MacBook-Pro.local""")
    except Exception:
        print "keypair create failed"
    return 'default_key'

def launch_gvl(tenant, password):
    client = OpenstackClient(tenant.region.name,
                             username=tenant.get_auth_username(),
                             password=tenant.auth_password,
                             project_name=tenant.get_tenant_name())

    nova = client.get_nova()
    key_name = add_keypair(nova)

    server_name = "bryn:%s group server" % (tenant.team.name)

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
s3_conn_path: /
s3_host: swift.rc.nectar.org.au
s3_port: 8888
bucket_default: cloudman-gvl-410
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
      archive_url: http://s3.climb.ac.uk/gvl/microgvl-fs-0.11-1-beta.tgz
      archive_md5: b116da95872802dfab5a22d8caec0f4a
    - name: gvl
      type: transient
      data_source: archive
      archive_url: http://s3.climb.ac.uk/gvl/microgvl-apps-0.11-1-beta.tgz
      archive_md5: 0c5421da6b4c432625159a9df6e12784
    - name: galaxyIndices
      type: transient
      roles: galaxyIndices
      archive_url: https://s3.eu-central-1.amazonaws.com/cloudman-gvl-400-frankfurt/gvl-indices-blank-4.0.0.tar.gz
      archive_md5: 09eadb352ef3be038221f4226edaadc8
  - name: Data
    filesystem_templates:
"""

    userdata = yaml.dump(user_specific_data, default_flow_style=False) + \
                 yaml.dump(cloud_specific_data, default_flow_style=False) + \
                 generic_data

    print userdata

    ## steps
    ## 1) find flavor
    ## 2) find network
    ## 3) allocate floating ip
    ## 4) launch

    #f = nova.floating_ips.create('public')
    #print f

    fl = nova.flavors.find(name='climb.group')

    #for i in client.get_glance().images.list():
    #    if i.name == 'GVL 4.1.0':
    #        image_id = i.id 

    #for n in nova.networks.list():
    #    print n.id, n.project_id
    #    if hasattr(n, 'tenant_id'):
    #        if n.tenant_id == default_tenant_id:
    #            print n

    cinder = client.get_cinder()

    volume = cinder.volumes.create(imageRef=tenant.region.regionsettings.gvl_image_id,
                                   name="bryn:%s boot volume" % (server_name,),
                                   size=120)
    cinder.volumes.set_bootable(volume, True)

    print volume.id
    for n in xrange(10):
        v = cinder.volumes.get(volume.id)
        print v.status
        time.sleep(1)


#[{"boot_index": "0", "uuid": "c19be03e-07fb-4d43-8531-c0bc1f8500e6", "volume_size": "120", "source_type": "volume", "destination_type": "volume", "delete_on_termination": false}]

    bdm = [{'uuid' : volume.id, 'source_type' : 'volume', 
           'destination_type' : 'volume',
           'boot_index' : "0",
           'delete_on_termination' : False}]

    server = nova.servers.create(server_name,
           "",
           flavor=fl,
    # birmingham
    #       nics=[{'net-id' : '1f12e463-50d1-4bd9-9d41-fa704be32b66'}],
    # cardiff - admin
    #       nics=[{'net-id' : '156d6c96-2dca-42a5-8fcd-803c0a1b8aa2'}],
    # cardiff - CLIMB_Demo
    #       nics=[{'net-id' : '935903a7-40f9-48eb-a80b-07869d569f3a'}],
    # warwick - public
           nics=[{'net-id' : '93ffd3af-c7cf-48d8-ba4c-ce59068c5c0a'}],           
           userdata=userdata,
           key_name=key_name,
           block_device_mapping_v2=bdm)
    print server

    #server.add_floating_ip(f.ip)

def run():
    team = Team.objects.get(pk=1)
    print team
    tenant = Tenant.objects.filter(team=team, region=Region.objects.get(name='warwick'))[0]
    print tenant
    launch_gvl(tenant, 'testtest99')
 
