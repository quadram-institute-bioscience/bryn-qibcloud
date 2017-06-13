import sshpubkeys

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from userdb.models import Region


SERVER_TYPE_CHOICES = [
    ('user', 'User server'),
    ('group', 'Group server'),
]


class LaunchServerForm(forms.Form):
    server_name = forms.CharField(
        label="Server name",
        max_length=50,
        required=True,
        validators=[RegexValidator(
            regex='^([a-zA-Z0-9\-]+)$',
            message="Only letters, numbers and hyphens in server name")])
    server_type = forms.ChoiceField(choices=SERVER_TYPE_CHOICES)

    password = forms.CharField(
        label="New server password",
        widget=forms.widgets.PasswordInput,
        required=True,
        validators=[RegexValidator(
          regex='^(?=.*[A-Z])(?=.*[0-9])(?=.*[a-z]).{8,}$',
          message="Weak password! At least one CAPITAL letter and one number required, minimum 8 characters.")])

class LaunchImageServerForm(forms.Form):
    server_name = forms.CharField(
        label="Server name",
        help_text="e.g. MyServer",
        max_length=50,
        required=True,
        validators=[RegexValidator(regex='^([a-zA-Z0-9\-]+)$',
                    message='Only letters, numbers & hyphens in server name')])
    server_type = forms.ChoiceField(choices=SERVER_TYPE_CHOICES)
    server_image = forms.ChoiceField(required=True)
    server_key_name_choice = forms.ChoiceField(
        required=True,
        label="SSH Key",
        help_text="Select an existing key, or make a new one")
    server_key_name = forms.CharField(
        label="New SSH Key Name",
        help_text="A descriptive name for your key (e.g. nickmacbook)",
        required=False)
    server_key = forms.CharField(
        label="SSH Public Key",
        help_text="Your SSH public key for access to the server.",
        widget=forms.Textarea,
        required=False)

    def __init__(self, images, keys, *args, **kwargs):
        super(LaunchImageServerForm, self).__init__(*args, **kwargs)
        self.fields['server_image'].choices = sorted(
            images, key=lambda i: i[1])
        self.fields['server_key_name_choice'].choices = keys + [
            ('bryn:new', 'Make new key')]

    def clean(self):
        cleaned_data = super(LaunchImageServerForm, self).clean()

        if cleaned_data['server_key_name_choice'] == 'bryn:new':
            if not cleaned_data['server_key_name']:
                self.add_error('server_key_name', ValidationError(
                    "Please enter a SSH key name", code='required'))
            if not cleaned_data['server_key']:
                self.add_error('server_key', ValidationError(
                    "Please enter a valid SSH public key", code='required'))
            else:
                try:
                    sshpubkeys.SSHKey(cleaned_data["server_key"]).parse()
                except (NotImplementedError, sshpubkeys.InvalidKeyException):
                    self.add_error('server_key', ValidationError(
                        "Please enter a valid SSH public key", code='invalid'))

        return cleaned_data


class RegionSelectForm(forms.Form):
    region = forms.ModelChoiceField(
        queryset=Region.objects.filter(disabled=False))
