from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from userdb.forms import InvitationForm
from django.http import HttpResponseRedirect, HttpResponseBadRequest,\
    JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from userdb.models import Team, Region, TeamMember
from openstack.models import Tenant, get_tenant_for_team
from forms import LaunchServerForm, LaunchImageServerForm
from scripts.list_instances import list_instances
from scripts.gvl_launch import launch_gvl
from scripts.image_launch import launch_image

from .utils import messages_to_json


def home(request):
    if not request.user.is_authenticated():
        form = AuthenticationForm()
        context = {'form': form}
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

            t.tenant_access = tenant

            t.instances = list_instances(tenant)

        context = {'invite': invite, 'teams': teams}
        return render(request, 'home/dashboard.html', context)


@login_required
def get_instances_table(request):
    if request.is_ajax():
        team = get_object_or_404(Team, pk=request.GET['team_id'])
        if not team.teammember_set.filter(user=request.user):
            return HttpResponseBadRequest
        tenant = get_tenant_for_team(team, Region.objects.get(name='warwick'))
        team.instances = list_instances(tenant)
        html = render_to_string(
            'home/includes/instances_table.html',
            {'t': team})
        return JsonResponse({'instances_table': html})
    else:
        return HttpResponseBadRequest


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


def validate_and_get_tenant(request, teamid):
    team = get_object_or_404(Team, pk=teamid)

    # check belongs to team
    member = TeamMember.objects.filter(team=team, user=request.user)
    if not member:
        messages.error(request, 'Access denied to this team.')
        return HttpResponseRedirect('/')

    tenant = get_tenant_for_team(team, Region.objects.get(name='warwick'))
    return tenant


@login_required
def launch(request, teamid):
    tenant = validate_and_get_tenant(request, teamid)

    f = LaunchServerForm(request.POST)
    if not f.is_valid():
        messages.error(request, 'Problem with form items.')
        return render(request, 'home/launch-fail.html', context={'form' : f})

    try:
        launch_gvl(tenant, f.cleaned_data['server_name'], f.cleaned_data['password'], f.cleaned_data['server_type'])
    except Exception, e:
        messages.error(request, 'Error launching: %s' % (e,))

    messages.success(request, 'Successfully launched server!')

    return HttpResponseRedirect('/')


@login_required
def launchcustom(request, teamid):
    tenant = validate_and_get_tenant(request, teamid)

    if request.method == 'POST':
        f = LaunchImageServerForm(tenant.get_images(), tenant.get_keys(), request.POST)
        if not f.is_valid():
            messages.error(request, 'Problem with form items.')
        else:
            try:
                if f.cleaned_data['server_key_name_choice'] == u'bryn:new':
                    key_name = f.cleaned_data['server_key_name']
                    key_value = f.cleaned_data['server_key']
                else:
                    key_name = f.cleaned_data['server_key_name_choice']
                    key_value = ''

                launch_image(tenant, f.cleaned_data['server_name'], f.cleaned_data['server_image'], key_name, key_value, f.cleaned_data['server_type'])
                return HttpResponseRedirect('/')
            except Exception, e:
                messages.error(request, 'Error launching: %s' % (e,))
            messages.success(request, 'Successfully launched server!')
    else:
        f = LaunchImageServerForm(tenant.get_images(), tenant.get_keys())
    return render(request, 'home/launch-image.html', context={'form' : f})
    launch_image(tenant, 'test-ubuntu', '2ae0fe84-74d9-47fe-a744-408ec28026fd', 'launchkey', 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQClUIKUlWckdyjIur2OhEFz4Xa2eKrpZe7ZgcVBnV3eUJi4WCPzB39aD4GvakwsUuKMGno3ipSCBI2Mcw2VfGD9oelCmPA/M6/cDvjijaQSgF5WBNoAbbaARtWyDSu+XMpbftNexmpc3CblamTm3DEgrOnhTcNJ+Imk+wBXpFUZOvfu/Ht/MBldbcgWp2RK8rgX+tCf5GUdgvA3Fz8YyvIOcIHIqSa9c9hfhes2hyLsrxe39norXUgsrgbMWlqqMYLc95TSYRFI+VYstoQ5b/6QHa/UloKkAR8LhVv8ntfRXVgvQtmUh3GzrYu326JW+kYSQ8hMX++v2w84vpL+50Rz nick@Nicks-MacBook-Pro.local', 'group')


def stop(request, teamid, uuid):
    tenant = validate_and_get_tenant(request, teamid)
    try:
        tenant.stop_server(uuid)
        messages.success(request, 'Server stopped.')
    except Exception, e:
        messages.error(request, e)
    if request.is_ajax():
        return JsonResponse(messages_to_json(request))
    else:
        return HttpResponseRedirect('/')


def start(request, teamid, uuid):
    tenant = validate_and_get_tenant(request, teamid)
    try:
        tenant.start_server(uuid)
        messages.success(request, 'Server started.')
    except Exception, e:
        messages.error(request, e)
    if request.is_ajax():
        return JsonResponse(messages_to_json(request))
    else:
        return HttpResponseRedirect('/')


def reboot(request, teamid, uuid):
    tenant = validate_and_get_tenant(request, teamid)
    try:
        tenant.reboot_server(uuid)
        messages.success(request, 'Server rebooted.')
    except Exception, e:
        messages.error(request, e)
    if request.is_ajax():
        return JsonResponse(messages_to_json(request))
    else:
        return HttpResponseRedirect('/')


def terminate(request, teamid, uuid): 
    tenant = validate_and_get_tenant(request, teamid)
    try:
        tenant.terminate_server(uuid)
        messages.success(request, 'Server terminated.')
    except Exception, e:
        messages.error(request, e)
    if request.is_ajax():
        return JsonResponse(messages_to_json(request))
    else:
        return HttpResponseRedirect('/')
