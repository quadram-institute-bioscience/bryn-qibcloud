from __future__ import unicode_literals

import uuid

from django.db.models import *
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string

from phonenumber_field.modelfields import PhoneNumberField


class Region(Model):
    name = CharField(max_length=40)
    description = CharField(max_length=40)
    disabled = BooleanField(default=False)
    disable_new_instances = BooleanField(default=False)

    def __str__(self):
        return self.name


class Institution(Model):
    name = CharField(max_length=100)


class Team(Model):
    name = CharField(max_length=50, verbose_name="Group or team name",
                     help_text="e.g. Bacterial pathogenomics group")
    creator = ForeignKey(User, on_delete=PROTECT)
    created_at = DateTimeField(auto_now_add=True)
    position = CharField(
        max_length=50,
        verbose_name="Position (e.g. Professor)")
    department = CharField(
        max_length=50,
        verbose_name="Department or Institute")
    institution = CharField(
        max_length=100,
        verbose_name="Institution (e.g. University of St. Elsewhere)")
    phone_number = PhoneNumberField(max_length=20, verbose_name="Phone number")
    research_interests = TextField(
        verbose_name="Research interests",
        help_text="Please supply a brief synopsis of your research programme")
    intended_climb_use = TextField(
        verbose_name="Intended use of CLIMB",
        help_text="Please let us know how you or your group intend to "
        "use CLIMB")
    held_mrc_grants = TextField(
        verbose_name="Held MRC grants",
        help_text="If you currently or recent have held grant funding from "
        "the Medical Research Council it would be very helpful if you can "
        "detail it here to assist with reporting use of CLIMB")
    verified = BooleanField(default=False)
    default_region = ForeignKey(Region, on_delete=PROTECT)
    tenants_available = BooleanField(default=False)

    def new_registration_admin_email(self):
        if not settings.NEW_REGISTRATION_ADMIN_EMAILS:
            return
        context = {'user': self.creator, 'team': self}
        subject = render_to_string(
            'userdb/email/new_registration_admin_subject.txt', context)
        text_content = render_to_string(
            'userdb/email/new_registration_admin_email.txt', context)
        html_content = render_to_string(
            'userdb/email/new_registration_admin_email.html', context)

        send_mail(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            settings.NEW_REGISTRATION_ADMIN_EMAILS,
            html_message=html_content,
            fail_silently=True
        )

    def verify_and_send_notification_email(self):
        context = {'user': self.creator, 'team': self}
        subject = render_to_string(
            'userdb/email/notify_team_verified_subject.txt', context)
        text_content = render_to_string(
            'userdb/email/notify_team_verified_email.txt', context)
        html_content = render_to_string(
            'userdb/email/notify_team_verified_email.html', context)

        send_mail(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [self.creator.email],
            html_message=html_content,
            fail_silently=False
        )

        self.verified = True
        self.save()

    def __str__(self):
        return self.name


class TeamMember(Model):
    team = ForeignKey(Team, on_delete=PROTECT)
    user = ForeignKey(User, on_delete=PROTECT)
    is_admin = BooleanField(default=False)

    def __str__(self):
        return "%s belongs to %s" % (self.user, self.team)


class Invitation(Model):
    uuid = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    to_team = ForeignKey(Team, on_delete=CASCADE,
                         verbose_name="Team to invite user to")
    made_by = ForeignKey(User, on_delete=CASCADE)
    email = EmailField()
    message = TextField()
    accepted = BooleanField()
    date = DateTimeField(auto_now_add=True)

    def send_invitation(self, user):
        self.made_by = user
        self.accepted = False
        self.save()

        context = {'invitation': self,
                   'url': reverse('user:accept-invite', args=[self.uuid])}
        subject = render_to_string(
            'userdb/email/user_invite_subject.txt', context)
        text_content = render_to_string(
            'userdb/email/user_invite_email.txt', context)
        html_content = render_to_string(
            'userdb/email/user_invite_email.html', context)

        send_mail(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            html_message=html_content,
            fail_silently=False
        )

    def __str__(self):
        return "%s to %s" % (self.email, self.to_team)


class UserProfile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    validation_link = UUIDField(primary_key=True, default=uuid.uuid4,
                                editable=False)
    email_validated = BooleanField(default=False)
    current_region = ForeignKey(Region, on_delete=PROTECT)

    def send_validation_link(self, user):
        self.user = user
        self.email_validated = False
        self.save()

        context = {'user': user,
                   'validation_link': reverse('user:validate-email',
                                              args=[self.validation_link])}
        subject = render_to_string(
            'userdb/email/user_verification_subject.txt', context)
        text_content = render_to_string(
            'userdb/email/user_verification_email.txt', context)
        html_content = render_to_string(
            'userdb/email/user_verification_email.html', context)

        send_mail(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_content,
            fail_silently=False
        )
