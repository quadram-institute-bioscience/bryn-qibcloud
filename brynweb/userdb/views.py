from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import Group

from .forms import CustomUserCreationForm, GroupProfileForm
from .models import Institution


def register(request):
    if request.method == 'POST':
        userform = CustomUserCreationForm(request.POST)
        profileform = GroupProfileForm(request.POST)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            group = Group()
            group.name = "%s research group" % (user.last_name)
            group.save()
            group.user_set.add(user)
            profile = profileform.save(commit=False)
            profile.group = group
            profile.save()

            messages.success(request, 'Thank you for registering. Your request will be approved by an administrator and you will receive an email with further instructions')

            return HttpResponseRedirect(reverse('home'))
    else:
        userform = CustomUserCreationForm()
        profileform = GroupProfileForm()

    return render(request, 'userdb/register.html',
                  {'userform': userform,
                   'profileform' : profileform})


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
