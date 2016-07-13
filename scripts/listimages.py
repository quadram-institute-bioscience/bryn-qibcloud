import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from brynweb.openstack.client import OpenstackClient, get_admin_credentials
from glanceclient import Client

client = OpenstackClient('warwick', **get_admin_credentials('warwick'))
glance = client.get_glance()

for i in glance.images.list():
    print i.__dict__
