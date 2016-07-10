import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from brynweb.openstack.client import OpenstackClient
import sys

client = OpenstackClient(sys.argv[1])
sess = client.get_sess()
print client.get_ec2_keys(sess.get_project_id())

