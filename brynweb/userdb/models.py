from __future__ import unicode_literals

from django.db.models import *
from django.contrib.auth.models import Group
from phonenumber_field.modelfields import PhoneNumberField

class Institution(Model):
    name = CharField(max_length=100)

class GroupProfile(Model):
    group = OneToOneField(Group, on_delete=CASCADE)

    position = CharField(max_length=50, verbose_name="Position (e.g. Professor)")
    department = CharField(max_length=50, verbose_name="Department or Institute")
    institution = CharField(max_length=100, verbose_name="Institution (e.g. University of St. Elsewhere)")
    phone_number = PhoneNumberField(max_length=20, verbose_name="Phone number")
    research_interests = TextField(verbose_name="Research interests", help_text="Please supply a brief synopsis of your research programme")
    intended_climb_use = TextField(verbose_name="Intended use of CLIMB", help_text="Please let us know how you or your group intend to use CLIMB")
    held_mrc_grants = TextField(verbose_name="Held MRC grants", help_text="If you currently or recent have held grant funding from the Medical Research Council it would be very helpful if you can detail it here to assist with reporting use of CLIMB")

