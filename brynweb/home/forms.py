
from django import forms
from django.forms.widgets import PasswordInput

class LaunchServerForm(forms.Form):
    server_name = forms.CharField(label='Server name', max_length=50)
    server_type = forms.ChoiceField(choices=(('group', 'Group server'), ('user', 'User server')))
    password = forms.CharField(label='New server password', widget=PasswordInput)

