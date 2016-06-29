from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from models import GroupProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = User

class GroupProfileForm(ModelForm):
    class Meta:
        model = GroupProfile
        exclude = ('user',)



