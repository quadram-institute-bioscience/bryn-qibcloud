from __future__ import unicode_literals

from django.db.models import *
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import uuid

from django.core.mail import send_mail
from django.core.urlresolvers import reverse

class Institution(Model):
    name = CharField(max_length=100)

class Team(Model):
    name = CharField(max_length=100, verbose_name="Group or team name", help_text="e.g. Bacterial pathogenomics group")

    creator = ForeignKey(User)
    created_at = DateTimeField(auto_now_add=True)

    position = CharField(max_length=50, verbose_name="Position (e.g. Professor)")
    department = CharField(max_length=50, verbose_name="Department or Institute")
    institution = CharField(max_length=100, verbose_name="Institution (e.g. University of St. Elsewhere)")
    phone_number = PhoneNumberField(max_length=20, verbose_name="Phone number")
    research_interests = TextField(verbose_name="Research interests", help_text="Please supply a brief synopsis of your research programme")
    intended_climb_use = TextField(verbose_name="Intended use of CLIMB", help_text="Please let us know how you or your group intend to use CLIMB")
    held_mrc_grants = TextField(verbose_name="Held MRC grants", help_text="If you currently or recent have held grant funding from the Medical Research Council it would be very helpful if you can detail it here to assist with reporting use of CLIMB")

    def __str__(self):
        return self.name

class TeamMember(Model):
    team = ForeignKey(Team)
    user = ForeignKey(User)
    is_admin = BooleanField(default=False)

    def __str__(self):
        return "%s belongs to %s" % (self.user, self.team)

class Invitation(Model):
    uuid = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    to_team = ForeignKey(Team, on_delete=CASCADE, verbose_name='Team to invite user to')
    made_by = ForeignKey(User, on_delete=CASCADE)
    email = EmailField()
    message = TextField()
    accepted = BooleanField()
    date = DateTimeField(auto_now_add=True)

    def send_invitation(self, user):
        self.made_by = user
        self.accepted = False
        self.save()

        send_mail('Invitation to join a CLIMB group',
                  """Hi there!

You have been invited by %s to become a member of the CLIMB team:

%s 

They also sent you a message:

%s

If you wish to become a member of this team and create a CLIMB account
then please visit the following link:

http://bryn.climb.ac.uk%s


Best regards

The CLIMB Project""" % (self.made_by.first_name, self.to_team.name, self.message, reverse('accept-invite', self.uuid)),
                    'noreply@discourse.climb.ac.uk',
                    [self.email], fail_silently=False)

    def __str__(self):
        return "%s to %s" % (self.email, self.to_team)
