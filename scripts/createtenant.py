import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from brynweb.openstack.client import get_keystone, get_nova
import sys

nova = get_nova(sys.argv[1])
keystone = get_keystone(sys.argv[1])

for t in keystone.tenants.list():
	if t.name.startswith('bryn:'):
		quota = nova.quotas.get(t.id)
		print quota
		quota.cores = 80
		nova.quotas.update(t.id, quota)

#keystone.tenants.create(tenant_name='bryn:test', description='test create tenant', enabled=True)
