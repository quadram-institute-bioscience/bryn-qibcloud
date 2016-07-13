from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from userdb.forms import InvitationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from userdb.models import Team, Region, TeamMember
from openstack.models import Tenant, get_tenant_for_team
from forms import LaunchServerForm
from scripts.list_instances import list_instances
from scripts.gvl_launch import launch_gvl

# Create your views here.

def home(request):
    if not request.user.is_authenticated():
        form = AuthenticationForm()
        context = {'form' : form}
        return render(request, 'home/home.html', context)
    else:
        invite = InvitationForm(request.user)

        teams = Team.objects.filter(teammember__user=request.user)
        for t in teams:
            if request.user == t.creator:
                t.is_admin = True

            t.form = LaunchServerForm()

            tenant = get_tenant_for_team(t, Region.objects.get(name='warwick'))
            if not tenant:
                messages.error(request, 'No tenant registered for this team!')
                continue

            t.instances = list_instances(tenant)

        context = {'invite' : invite, 'teams' : teams}
        return render(request, 'home/dashboard.html', context)

def loginpage(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.userprofile.email_validated:
            if user.is_active:
                login(request, user)
                messages.success(request, 'You have been successfully logged in.')
            else:
                messages.error(request, 'Sorry your account is disabled.')
        else:
            messages.error(request, 'Please validate your email address by following the link sent to your email first.')
    else:
        messages.error(request, 'Invalid username or password.')
    return HttpResponseRedirect('/')

def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def launch(request, teamid):
    team = get_object_or_404(Team, pk=teamid)

    # check belongs to team
    member = TeamMember.objects.filter(team=team, user=request.user) 
    if not member:
        messages.error(request, 'Access denied to this team.')
        return HttpResponseRedirect('/')

    f = LaunchServerForm(request.POST)
    if not f.is_valid():
        messages.error(request, 'Problem with form items.')
        return HttpResponseRedirect('/')

    tenant = get_tenant_for_team(team, Region.objects.get(name='warwick'))
    launch_gvl(tenant, f.cleaned_data['server_name'], f.cleaned_data['password'], f.cleaned_data['server_type'])

    messages.success(request, 'Successfully launched server!')

    return HttpResponseRedirect('/')
 
