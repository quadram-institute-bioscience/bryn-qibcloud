from openstack.client import OpenstackClient, get_admin_credentials
from openstack.models import Tenant

def run():
    client = OpenstackClient('cardiff', **get_admin_credentials('cardiff'))
    neutron = client.get_neutron()
    routers = neutron.list_routers(name='tenant1-router')

    network_ids = []
    for network in neutron.list_networks(name='tenant1-private')['networks']:
        network_ids.append(network['id'])

    ports = neutron.list_ports()
    for port in ports['ports']:
        if port['network_id'] in network_ids:
            print port
            neutron.delete_port(port['id'])
        else:
            print "port not in network"

#    for router in routers['routers']:
#        neutron.delete_router(router['id'])

#    for network in neutron.list_networks(name='tenant1-private')['networks']:
#        neutron.delete_network(network['id'])

