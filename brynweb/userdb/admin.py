from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect

from userdb.models import Team, Invitation, TeamMember, UserProfile

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'creator', 'created_at', 'verified')
    list_filter = ('verified',)

    actions = ['setup_teams',]

    def setup_teams(self, request, queryset):
        teams = [str(t.pk) for t in queryset]
        return HttpResponseRedirect("/setup/?ids=%s" % (",".join(teams)))

# Re-register GroupAdmin
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember)
admin.site.register(Invitation)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

