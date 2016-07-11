from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from userdb.forms import InvitationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

def home(request):
    if not request.user.is_authenticated():
        form = AuthenticationForm()
        context = {'form' : form}
        return render(request, 'home/home.html', context)
    else:
        invite = InvitationForm(request.user)
        context = {'invite' : invite}
        return render(request, 'home/dashboard.html', context)

def loginpage(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            messages.success(request, 'You have been successfully logged in.')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Sorry your account is disabled.')
    else:
        messages.error(request, 'Invalid username or password.')
    return HttpResponseRedirect('/')
