
from django import forms
from django.forms.widgets import PasswordInput
from django.core.validators import RegexValidator

class LaunchServerForm(forms.Form):
    server_name = forms.CharField(label='Server name', max_length=50, required=True,
                              validators=[
                                RegexValidator(
                                     regex='^([a-zA-Z0-9\-]+)$',
                                     message='Only letters, numbers and hyphens in server name',
                                )
                              ])
    server_type = forms.ChoiceField(choices=(('group', 'Group server'), ('user', 'User server')))

    password = forms.CharField(label='New server password', widget=PasswordInput, required=True)

