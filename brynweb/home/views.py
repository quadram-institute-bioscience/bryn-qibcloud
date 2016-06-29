from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

# Create your views here.

def home(request):
	form = AuthenticationForm()
	context = {'form' : form}
	return render(request, 'home/home.html', context)

def loginpage(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse('logged in')
        else:
            return HttpResponse('disabled account')
    else:
        return HttpResponse('invalid login')

