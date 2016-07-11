from django.shortcuts import render
from django.http import HttpResponse
from openstack.client import OpenstackClient

# Create your views here.

def index(request):
        client = OpenstackClient(request.GET.get('region', 'bham'))
	servers = client.get_servers()
	context = {'servers': servers}
	return render(request, 'reporting/servers.html', context)

