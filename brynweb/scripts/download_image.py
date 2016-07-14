
from openstack.client import OpenstackClient, get_admin_credentials
from openstack.models import Tenant
from userdb.models import Team, Region
import sys
import yaml
import pprint

def download_instance(imageid):
    client = OpenstackClient('warwick', **get_admin_credentials('warwick'))

    glance = client.get_glance()
    image = glance.images.get(imageid)

    file_name = "gwas.img"
    image_file = open(file_name, 'w+')

    for chunk in image.data():
        image_file.write(chunk)

    image_file.close()

def run():
    download_instance('cf9b9388-8553-4103-8955-d0348ce4cd80')
