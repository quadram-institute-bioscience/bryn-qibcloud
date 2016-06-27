
from novaclient import client
from keystoneauth1 import loading
from keystoneauth1 import session
from pprint import pprint
from keystoneclient.v2_0 import client as keystoneclient
import settings
import sys

def get_servers(region):
	authsettings = settings.AUTHENTICATION[region]

	loader = loading.get_plugin_loader('password')
	auth = loader.load_from_options(auth_url=authsettings['AUTH_URL'],
									username=authsettings['AUTH_NAME'],
									password=authsettings['AUTH_PASSWORD'],
					                project_name=authsettings['TENANT_NAME'])
	sess = session.Session(auth=auth)

	nova = client.Client(2, session=sess, insecure=True)
	keystone = keystoneclient.Client(session=sess)

	search_opts = { 'all_tenants': True, }

	servers = nova.servers.list(detailed=True, search_opts=search_opts)

	tenants = {}
	for s in servers:
		if s.tenant_id not in tenants:
			tenants[s.tenant_id] = keystone.tenants.get(s.tenant_id)
		s.tenant = tenants[s.tenant_id]

	users = {}
	for s in servers:
		if s.user_id not in users:
			users[s.user_id] = keystone.users.get(s.user_id)
		s.user = users[s.user_id]


	return servers

servers = get_servers(sys.argv[1])
for s in servers:
	print s.name, s.tenant, s.user, s._info['OS-EXT-SRV-ATTR:host']
##user_id
	##s, nova.flavors.get(s.flavor['id'])
##	print nova.flavors.list()

"""
{ 'OS-DCF:diskConfig': u'AUTO',
  'OS-EXT-AZ:availability_zone': u'nova',
  'OS-EXT-SRV-ATTR:host': u'cl0901u01.climb.cluster',
  'OS-EXT-SRV-ATTR:hypervisor_hostname': u'cl0901u01.climb.cluster',
  'OS-EXT-SRV-ATTR:instance_name': u'instance-00000462',
  'OS-EXT-STS:power_state': 1,
  'OS-EXT-STS:task_state': None,
  'OS-EXT-STS:vm_state': u'active',
  'OS-SRV-USG:launched_at': u'2015-05-26T11:12:00.000000',
  'OS-SRV-USG:terminated_at': None,
  '_info': { u'OS-DCF:diskConfig': u'AUTO',
             u'OS-EXT-AZ:availability_zone': u'nova',
             u'OS-EXT-SRV-ATTR:host': u'cl0901u01.climb.cluster',
             u'OS-EXT-SRV-ATTR:hypervisor_hostname': u'cl0901u01.climb.cluster',
             u'OS-EXT-SRV-ATTR:instance_name': u'instance-00000462',
             u'OS-EXT-STS:power_state': 1,
             u'OS-EXT-STS:task_state': None,
             u'OS-EXT-STS:vm_state': u'active',
             u'OS-SRV-USG:launched_at': u'2015-05-26T11:12:00.000000',
             u'OS-SRV-USG:terminated_at': None,
             u'accessIPv4': u'',
             u'accessIPv6': u'',
             u'addresses': { u'192.168.100.0/24': [ { u'OS-EXT-IPS-MAC:mac_addr': u'fa:16:3e:fd:b6:6b',
                                                      u'OS-EXT-IPS:type': u'fixed',
                                                      u'addr': u'192.168.100.13',
                                                      u'version': 4},
                                                    { u'OS-EXT-IPS-MAC:mac_addr': u'fa:16:3e:fd:b6:6b',
                                                      u'OS-EXT-IPS:type': u'floating',
                                                      u'addr': u'147.188.173.131',
                                                      u'version': 4}]},
             u'config_drive': u'',
             u'created': u'2015-05-08T11:47:16Z',
             u'flavor': { u'id': u'88cec1f0-859f-49ac-9ff5-5881ad4d51c3',
                          u'links': [ { u'href': u'http://climb-bham-nova.climb.cluster:8774/945224455dde451b9c2078279f327f28/flavors/88cec1f0-859f-49ac-9ff5-5881ad4d51c3',
                                        u'rel': u'bookmark'}]},
             u'hostId': u'6809ce4ac0d4914db0ab34c9356858177fe492d39de1b6ddff22c8d3',
             u'id': u'00d3c8e0-6a3c-478c-b3e6-21e08ecffe57',
             u'image': { u'id': u'0f68831a-2c4a-488f-9a94-07a714c87cd1',
                         u'links': [ { u'href': u'http://climb-bham-nova.climb.cluster:8774/945224455dde451b9c2078279f327f28/images/0f68831a-2c4a-488f-9a94-07a714c87cd1',
                                       u'rel': u'bookmark'}]},
             u'key_name': u'roy',
             u'links': [ { u'href': u'http://climb-bham-nova.climb.cluster:8774/v2/945224455dde451b9c2078279f327f28/servers/00d3c8e0-6a3c-478c-b3e6-21e08ecffe57',
                           u'rel': u'self'},
                         { u'href': u'http://climb-bham-nova.climb.cluster:8774/945224455dde451b9c2078279f327f28/servers/00d3c8e0-6a3c-478c-b3e6-21e08ecffe57',
                           u'rel': u'bookmark'}],
             u'metadata': { },
             u'name': u'microbesng',
             u'os-extended-volumes:volumes_attached': [ { u'id': u'919e49aa-7324-4dcf-857e-5bf48eef74ec'}],
             u'progress': 0,
             u'security_groups': [{ u'name': u'microbesng'}],
             u'status': u'ACTIVE',
             u'tenant_id': u'6f205752d4d9413a97b181a540c037e4',
             u'updated': u'2015-12-18T16:25:01Z',
             u'user_id': u'dc7a800caa9444f8ba80f54bf3816e70'},
  '_loaded': True,
  'accessIPv4': u'',
  'accessIPv6': u'',
  'addresses': { u'192.168.100.0/24': [ { u'OS-EXT-IPS-MAC:mac_addr': u'fa:16:3e:fd:b6:6b',
                                          u'OS-EXT-IPS:type': u'fixed',
                                          u'addr': u'192.168.100.13',
                                          u'version': 4},
                                        { u'OS-EXT-IPS-MAC:mac_addr': u'fa:16:3e:fd:b6:6b',
                                          u'OS-EXT-IPS:type': u'floating',
                                          u'addr': u'147.188.173.131',
                                          u'version': 4}]},
  'config_drive': u'',
  'created': u'2015-05-08T11:47:16Z',
  'flavor': { u'id': u'88cec1f0-859f-49ac-9ff5-5881ad4d51c3',
              u'links': [ { u'href': u'http://climb-bham-nova.climb.cluster:8774/945224455dde451b9c2078279f327f28/flavors/88cec1f0-859f-49ac-9ff5-5881ad4d51c3',
                            u'rel': u'bookmark'}]},
  'hostId': u'6809ce4ac0d4914db0ab34c9356858177fe492d39de1b6ddff22c8d3',
  'id': u'00d3c8e0-6a3c-478c-b3e6-21e08ecffe57',
  'image': { u'id': u'0f68831a-2c4a-488f-9a94-07a714c87cd1',
             u'links': [ { u'href': u'http://climb-bham-nova.climb.cluster:8774/945224455dde451b9c2078279f327f28/images/0f68831a-2c4a-488f-9a94-07a714c87cd1',
                           u'rel': u'bookmark'}]},
  'key_name': u'roy',
  'links': [ { u'href': u'http://climb-bham-nova.climb.cluster:8774/v2/945224455dde451b9c2078279f327f28/servers/00d3c8e0-6a3c-478c-b3e6-21e08ecffe57',
               u'rel': u'self'},
             { u'href': u'http://climb-bham-nova.climb.cluster:8774/945224455dde451b9c2078279f327f28/servers/00d3c8e0-6a3c-478c-b3e6-21e08ecffe57',
               u'rel': u'bookmark'}],
  'manager': <novaclient.v2.servers.ServerManager object at 0x7fc0ea699310>,
  'metadata': { },
  'name': u'microbesng',
  'os-extended-volumes:volumes_attached': [ { u'id': u'919e49aa-7324-4dcf-857e-5bf48eef74ec'}],
  'progress': 0,
  'security_groups': [{ u'name': u'microbesng'}],
  'status': u'ACTIVE',
  'tenant_id': u'6f205752d4d9413a97b181a540c037e4',
  'updated': u'2015-12-18T16:25:01Z',
  'user_id': u'dc7a800caa9444f8ba80f54bf3816e70',
  'x_openstack_request_ids': []}
"""
