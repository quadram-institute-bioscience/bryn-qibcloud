
from openstack.client import OpenstackClient, get_admin_credentials
from openstack.models import HypervisorStats
from userdb.models import Team, Region
import sys
import yaml
import pprint
import os

def run():
    for region in Region.objects.all():
        #if not region.disabled:
        if 1:
            client = OpenstackClient(region.name, **get_admin_credentials(region.name))
            nova = client.get_nova()

            stats = nova.hypervisors.statistics()

            try:
                h = HypervisorStats.objects.get(region=region)
            except HypervisorStats.DoesNotExist:
                h = HypervisorStats(region=region)

            print stats.__dict__
            h.hypervisor_count = stats.count
            h.disk_available_least = stats.disk_available_least
            h.free_disk_gb = stats.free_disk_gb
            h.free_ram_mb = stats.free_ram_mb
            h.local_gb = stats.local_gb
            h.local_gb_used = stats.local_gb_used
            h.memory_mb = stats.memory_mb  
            h.memory_mb_used = stats.memory_mb_used
            h.running_vms = stats.running_vms
            h.vcpus = stats.vcpus
            h.vcpus_used = stats.vcpus_used

            h.save() 
