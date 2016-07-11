from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group

from userdb.models import Team, Invitation, TeamMember

# Re-register GroupAdmin
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Invitation)

