
def add_floating_ip(nova, tenant, server):
    if tenant.region.regionsettings.requires_network_setup:

        # attempt to reuse existing unassigned flaoting IPs
        fixed_ip_list = nova.floating_ips.list()
        for ip in fixed_ip_list:
            if ip.fixed_ip is None and ip.instance_id is None:
                server.add_floating_ip(ip)
                return

        # else create a new one
        f = nova.floating_ips.create(tenant.region.regionsettings.floating_ip_pool)
        server.add_floating_ip(f)

def add_keypair(nova, keyname, keyvalue):
    for k in nova.keypairs.list():
        if k.name == keyname:
            return k.name

    keypair = nova.keypairs.create(name=keyname, public_key=keyvalue)
    return keyname

