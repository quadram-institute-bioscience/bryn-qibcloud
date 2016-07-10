import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from brynweb.openstack.client import OpenstackClient
import sys
import yaml

# not used share_string, custom_image_id

## info to collect

## image_id
## tenant_id
## access_key
## secret_key
## key-name

client = OpenstackClient(sys.argv[1])

key_name = 'cloudman_key_pair'

user_specific_data = {'cloud_name'   : 'CLIMB',
                      'cluster_name' : 'GVL group',
                      'key_name'     : key_name,
                      'password'     : 'testtest',
                      'freenxpass'   : 'testtest'}

default_tenant_id = client.get_sess().get_project_id()

access, secret = client.get_ec2_keys(default_tenant_id)

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

nova = client.get_nova()

## steps
## 1) find flavor
## 2) find network
## 3) allocate floating ip
## 4) launch

#f = nova.floating_ips.create('public')
#print f

fl = nova.flavors.find(name='climb.group')

for i in client.get_glance().images.list():
    if i.name == 'GVL 4.1.0':
        image_id = i.id 

for n in nova.networks.list():
    print n.id, n.project_id
    if hasattr(n, 'tenant_id'):
        if n.tenant_id == default_tenant_id:
            print n

server = nova.servers.create('test-gvl',
       flavor=fl,
       image=image_id,
# birmingham
#       nics=[{'net-id' : '1f12e463-50d1-4bd9-9d41-fa704be32b66'}],
# cardiff - admin
#       nics=[{'net-id' : '156d6c96-2dca-42a5-8fcd-803c0a1b8aa2'}],
# cardiff - CLIMB_Demo
       nics=[{'net-id' : '935903a7-40f9-48eb-a80b-07869d569f3a'}],
       userdata=userdata,
       key_name=key_name,
    )
print server

#server.add_floating_ip(f.ip)

