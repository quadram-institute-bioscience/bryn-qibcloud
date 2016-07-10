import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from brynweb.openstack.client import get_sess
from glanceclient import Client

sess = get_sess(sys.argv[1])
glance = Client('2', session=sess)

image = glance.images.create(name="myNewImage")
glance.images.upload(image.id, open(sys.argv[2], 'rb'))

