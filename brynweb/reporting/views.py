from django.shortcuts import render
from django.http import HttpResponse
from openstack.client import get_servers

# Create your views here.

def index(request):
	servers = get_servers(request.GET.get('region', 'bham'))
	context = {'servers': servers}
	return render(request, 'reporting/servers.html', context)

