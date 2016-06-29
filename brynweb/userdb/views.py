from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import CustomUserCreationForm, GroupProfileForm

def register(request):
    if request.method == 'POST':
        userform = CustomUserCreationForm(request.POST)
        profileform = GroupProfileForm(request.POST)
        if form.is_valid():
            return HttpResponse('registered')
    else:
        userform = CustomUserCreationForm()
        profileform = GroupProfileForm()

    return render(request, 'userdb/register.html',
                  {'userform': userform,
                   'profileform' : profileform})
