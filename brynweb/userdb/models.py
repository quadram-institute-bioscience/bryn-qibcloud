from __future__ import unicode_literals

from django.db.models import *
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Institution(Model):
    name = CharField(max_length=100)


class GroupProfile(Model):
    user = OneToOneField(User, on_delete=CASCADE)

    position = CharField(max_length=50)
    department = CharField(max_length=50)
    institution = CharField(max_length=100)
    phone_number = PhoneNumberField(max_length=20)
    research_interests = TextField()
    intended_climb_use = TextField()
    held_mrc_grants = TextField()

    def __unicode__(self):
        return self.user.get_full_name()

