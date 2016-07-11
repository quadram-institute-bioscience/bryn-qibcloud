from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin

from userdb.models import Team, Invitation, TeamMember, UserProfile

# Re-register GroupAdmin
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Invitation)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

