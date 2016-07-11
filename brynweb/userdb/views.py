from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, TeamForm, InvitationForm
from .models import Institution, Team, TeamMember, Invitation


def register(request):
    if request.method == 'POST':
        userform = CustomUserCreationForm(request.POST)
        teamform = TeamForm(request.POST)
        if userform.is_valid() and teamform.is_valid():
            user = userform.save()

            # add team
            team = teamform.save(commit=False)
            team.creator = user
            team.save()

            # add team member
            member = TeamMember()
            member.team = team
            member.user = user
            member.is_admin = True
            member.save()

            messages.success(request, 'Thank you for registering. Your request will be approved by an administrator and you will receive an email with further instructions')

            return HttpResponseRedirect(reverse('home'))
    else:
        userform = CustomUserCreationForm()
        teamform = TeamForm()

    return render(request, 'userdb/register.html',
                  {'userform': userform,
                   'teamform' : teamform})

@login_required
def invite(request):
    if request.method == 'POST':
        form = InvitationForm(request.user, request.POST)
        if form.is_valid():
            print form.cleaned_data['email']
            print form.cleaned_data['to_team']
            if Invitation.objects.filter(email=form.cleaned_data['email'], to_team=form.cleaned_data['to_team']):
                messages.error(request, 'User has already been invited to this team.')
            else:
                invitation = form.save(commit=False)
                invitation.send_invitation(request.user)

                messages.success(request, 'Invitation sent.')
    else:
        messages.error(request, 'No information supplied for invitation')
    return HttpResponseRedirect(reverse('home'))

def institution_typeahead(request):
    q = request.GET.get('q', '')
    if q:
        matches = (Institution.objects
                   .filter(name__icontains=q)
                   .values_list('name', flat=True)[:10])
    else:
        matches = Institution.objects.all().values_list('name', flat=True)
    data = list(matches)
    return JsonResponse(data, safe=False)


def accept_invite(request, uuid):
    return HttpResponse(uuid)


