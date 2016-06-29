from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from forms import CustomUserCreationForm, GroupProfileForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        userform = CustomUserCreationForm(request.POST)
        profileform = GroupProfileForm(request.POST)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            profileform.user = user
            profileform.save()

            messages.success(request, 'Thank you for registering. Your request will be approved by an administrator and you will receive an email with further instructions')

            return HttpResponseRedirect(reverse('home'))
    else:
        userform = CustomUserCreationForm()
        profileform = GroupProfileForm()

    return render(request, 'userdb/register.html',
                  {'userform': userform,
                   'profileform' : profileform})
