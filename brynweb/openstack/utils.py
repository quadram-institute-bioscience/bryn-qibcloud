
def add_floating_ip(tenant, server):
    if tenant.region.regionsettings.requires_network_setup:
        f = nova.floating_ips.create(tenant.region.regionsettings.floating_ip_pool)
        server.add_floating_ip(f)

def add_keypair(nova, keyname, keyvalue):
    for k in nova.keypairs.list():
        if k.name == keyname:
            return k.name

    keypair = nova.keypairs.create(name=keyname, public_key=keyvalue)
    return keyname

