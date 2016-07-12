from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from .models import Team, Invitation, TeamMember

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        model = User

class TeamForm(ModelForm):
    class Meta:
        model = Team
        exclude = ('creator', 'created_at', 'verified', 'default_region')
        widgets = {'phone_number': PhoneNumberInternationalFallbackWidget}

class InvitationForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super (InvitationForm,self ).__init__(*args,**kwargs) 

        self.fields['to_team'].queryset = Team.objects.filter(teammember__user=user, teammember__is_admin=True)
        self.fields['to_team'].empty_label = None

    class Meta:
        model = Invitation
        fields = ('to_team', 'email', 'message')


