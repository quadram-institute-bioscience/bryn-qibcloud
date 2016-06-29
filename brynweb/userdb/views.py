from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from forms import CustomUserCreationForm, GroupProfileForm

def register(request):
    if request.method == 'POST':
        userform = CustomUserCreationForm(request.POST)
        profileform = GroupProfileForm(request.POST)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            profileform.user = user
            profileform.save()

            return HttpResponse('registered')
    else:
        userform = CustomUserCreationForm()
        profileform = GroupProfileForm()

    return render(request, 'userdb/register.html',
                  {'userform': userform,
                   'profileform' : profileform})
