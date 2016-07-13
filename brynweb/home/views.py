from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from userdb.forms import InvitationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse

from userdb.models import Team

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
    
    
