import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from brynweb.openstack.client import get_nova

nova = get_nova(sys.argv[1])
fl = nova.flavors.find(name='climb.group')

# destroy all servers
#for s in nova.servers.list(search_opts={'flavor' : fl.id}):
#	print "deleting %s" % (s,)
#	nova.servers.delete(s)

for n in xrange(1,int(sys.argv[2])):
    print nova.servers.create('test-automation%d' % (n,),
       flavor=fl,
       image=regions[sys.argv[1]]['image_id'],
       nics=[{'net-id' : 'd0569e32-25d4-427f-af64-dce9d55ee398'}]
    )
    ##,
    ##   network='93ffd3af-c7cf-48d8-ba4c-ce59068c5c0a',
    ##   nics=[{'net-id' : '93ffd3af-c7cf-48d8-ba4c-ce59068c5c0a'}]
    ##)
