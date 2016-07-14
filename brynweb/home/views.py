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
from forms import LaunchServerForm, LaunchImageServerForm, RegionSelectForm
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
        region = request.user.userprofile.current_region

        invite = InvitationForm(request.user)

        teams = Team.objects.filter(teammember__user=request.user)

        regionform = RegionSelectForm()
        regionform.initial['region'] = region

        for t in teams:
            if request.user == t.creator:
                t.is_admin = True

            t.active = True
            tenant = get_tenant_for_team(t, region)
            if not tenant:
                t.active = False
                messages.error(request, 'No tenant registered for this team!')
                continue

            if region.name == 'bham':
                t.horizon_endpoint = 'http://birmingham.climb.ac.uk'
            elif region.name == 'cardiff':
                t.horizon_endpoint = 'http://cardiff.climb.ac.uk'
            elif region.name == 'warwick':
                t.horizon_endpoint = 'http://stack.warwick.climb.ac.uk'
   
            t.launch_form = LaunchServerForm()
            t.launch_custom_form = LaunchImageServerForm(tenant.get_images(), tenant.get_keys())
            t.tenant_access = tenant
            t.instances = list_instances(tenant)

        context = {'invite': invite, 'teams': teams, 'regionform' : regionform}
        return render(request, 'home/dashboard.html', context)


@login_required
def get_instances_table(request):
    if request.is_ajax():
        team = get_object_or_404(Team, pk=request.GET.get('team_id'))
        if not team.teammember_set.filter(user=request.user):
            return HttpResponseBadRequest
        tenant = get_tenant_for_team(team, request.user.userprofile.current_region)
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

    region = request.user.userprofile.current_region
    tenant = get_tenant_for_team(team, region)
    return tenant


@login_required
def launch(request, teamid):
    tenant = validate_and_get_tenant(request, teamid)

    f = LaunchServerForm(request.POST)
    if not f.is_valid():
        if request.is_ajax():
            return JsonResponse({'errors': f.errors}, status=400)
        messages.error(request, 'Problem with form items.')
        return render(request, 'home/launch-fail.html', context={'form': f})

    try:
        launch_gvl(tenant, f.cleaned_data['server_name'], f.cleaned_data['password'], f.cleaned_data['server_type'])
    except Exception, e:
        messages.error(request, 'Error launching: %s' % (e,))
    else:
        messages.success(request, 'Successfully launched server!')

    if request.is_ajax():
        return JsonResponse(messages_to_json(request))
    else:
        return HttpResponseRedirect('/')


@login_required
def launchcustom(request, teamid):
    tenant = validate_and_get_tenant(request, teamid)

    if request.method == 'POST':
        f = LaunchImageServerForm(tenant.get_images(), tenant.get_keys(), request.POST)
        if not f.is_valid():
            if request.is_ajax():
                return JsonResponse({'errors': f.errors}, status=400)
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
            except Exception, e:
                messages.error(request, 'Error launching: %s' % (e,))
            else:
                messages.success(request, 'Successfully launched server!')

        if request.is_ajax():
            return JsonResponse(messages_to_json(request))
        else:
            return HttpResponseRedirect('/')
    else:
        f = LaunchImageServerForm(tenant.get_images(), tenant.get_keys())
    return render(request, 'home/launch-image.html', context={'form' : f})

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def region_select(request):
    if request.method == 'POST':
        f = RegionSelectForm(request.POST)
        if f.is_valid():
            userprofile = request.user.userprofile
            userprofile.current_region = f.cleaned_data['region']
            userprofile.save()
            messages.success(request, 'Region changed to %s' % (f.cleaned_data['region']))

    return HttpResponseRedirect('/')
