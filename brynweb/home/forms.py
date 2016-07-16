
from django import forms
from django.forms.widgets import PasswordInput
from django.core.validators import RegexValidator
from userdb.models import Region

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

class LaunchImageServerForm(forms.Form):
    def __init__(self, images, keys, *args, **kwargs):
        super(LaunchImageServerForm, self).__init__(*args, **kwargs)
        self.fields['server_image'].choices = images
        print type(keys)
        self.fields['server_key_name_choice'].choices = keys + [('bryn:new', 'Make new key'),]

    def clean(self):
        form_data = self.cleaned_data
        if form_data['server_key_name_choice'] == 'bryn:new':
            if not form_data['server_key_name']:
                self._errors["server_key_name"] = ["Please specify a key name"]
            if not form_data['server_key']:
                self._errors["server_key"] = ["Please specify a server key value"]
        return form_data

    server_name = forms.CharField(label='Server name', max_length=50, required=True,
                              validators=[
                                RegexValidator(
                                     regex='^([a-zA-Z0-9\-]+)$',
                                     message='Only letters, numbers and hyphens in server name',
                                )
                              ])
    server_type = forms.ChoiceField(choices=(('group', 'Group server'), ('user', 'User server')))
    server_image = forms.ChoiceField(required=True)

    server_key_name_choice = forms.ChoiceField(required=True)
    server_key_name = forms.CharField(label='Server key name', help_text='A descriptive name for your key', required=False)
    server_key = forms.CharField(label='Server key', help_text='Your SSH public server key for access to the serer.', widget=forms.Textarea, required=False)

class RegionSelectForm(forms.Form):
    region = forms.ModelChoiceField(queryset=Region.objects.filter(disabled=False))
