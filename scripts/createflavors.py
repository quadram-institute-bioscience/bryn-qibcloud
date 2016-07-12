import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from novaclient import client
from keystoneauth1 import loading
from keystoneauth1 import session
from pprint import pprint
from keystoneclient.v2_0 import client as keystoneclient
from brynweb.openstack.client import get_nova
import sys

nova = get_nova(sys.argv[1])
print nova.flavors.list()

nova.flavors.create(name  = 'climb.group',
                    ram   = 64 * 1024,
                    vcpus = 8,
                    disk  = 120,
                    swap  = 0)

nova.flavors.create(name  = 'climb.user',
                    ram   = 32 * 1024,
                    vcpus = 4,
                    disk  = 120,
                    swap  = 0)

