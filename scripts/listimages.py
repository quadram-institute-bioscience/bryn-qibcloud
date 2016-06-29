import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from brynweb.openstack.client import get_sess
from glanceclient import Client

sess = get_sess(sys.argv[1])
glance = Client('2', session=sess)
for i in glance.images.list():
	print i

