import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from brynweb.openstack.client import get_nova
import sys

nova = get_nova(sys.argv[1])

f = nova.floating_ips.create('public')
print f

for f in nova.floating_ips.list():
	print f

