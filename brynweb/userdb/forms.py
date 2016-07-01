from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from .models import GroupProfile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = User


class GroupProfileForm(ModelForm):
    class Meta:
        model = GroupProfile
        exclude = ('user',)
        widgets = {'phone_number': PhoneNumberInternationalFallbackWidget}
