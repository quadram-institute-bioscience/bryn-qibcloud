import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from brynweb.openstack.client import OpenstackClient
import sys

# add a user
# make tenant
# set quota
# set access control
# set up networking (for bham, cardiff)
# add key pair (optional)

client = OpenstackClient(sys.argv[1])
tenant_name = sys.argv[2]
nova = client.get_nova()
keystone = client.get_keystone()

for t in keystone.tenants.list():
    if t.description.startswith('bryn:'):
        print "remove %s" % ( t.name, )
        t.delete()

for u in keystone.users.list():
    if u.name.startswith('bryn:'):
        print "remove %s" % ( u.name, )
        u.delete()

t = keystone.tenants.create(tenant_name=tenant_name, description='bryn: test create tenant', enabled=True)
keystone.users.create(name='bryn:test', password='bryn:test', tenant_id=t.id)

neutron = client.get_neutron()

network = {'tenant_id'      : t.id,
           'name'           : 'tenant1-private',
           'admin_state_up' : True}
n = neutron.create_network({'network':network})

router = {"tenant_id"      : t.id,
          "name"           : "tenant1-router",
          "admin_state_up" : True}
r = neutron.create_router({'router':router})

public_network = '311a2f36-b913-4b7c-94aa-e4d433985012'

neutron.add_gateway_router(r['router']['id'], {"network_id" : public_network})

print t.id

# add subnet

subnet = {"name": "tenant1-192.168.0.0/24",
          "enable_dhcp": True,
          "network_id": n['network']['id'],
          "tenant_id": t.id,
          "allocation_pools": [{"start": "192.168.0.50", "end": "192.168.0.200"}],
          "gateway_ip": "192.168.0.1",
          "ip_version": 4,
          "cidr": "192.168.0.0/24"}

s = neutron.create_subnet({'subnet' : subnet})

# router-interface-add

neutron.add_interface_router(r['router']['id'], {'subnet_id' : s['subnet']['id']})

"""
neutron net-create tenant1-private --tenant-id 6847328801474250af62e4cbfb7b661f
neutron router-create --tenant-id 6847328801474250af62e4cbfb7b661f tenant1-router
neutron router-gateway-set tenant1-router public
neutron subnet-create  tenant1-private 192.168.0.0/24 --tenant-id 6847328801474250af62e4cbfb7b661f --name "tenant1-192.168.0.0/24" --gateway 192.168.0.1  --allocation-pool start=192.168.0.50,end=192.168.0.200 --enable-dhcp  --ip-version 4
neutron router-interface-add tenant1-router "tenant1-192.168.0.0/24"
"""

#	if t.name.startswith('bryn:'):
#		quota = nova.quotas.get(t.id)
#		print quota
#		quota.cores = 80
#		nova.quotas.update(t.id, quota)

#keystone.tenants.create(tenant_name='bryn:test', description='test create tenant', enabled=True)
