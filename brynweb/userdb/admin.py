from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect

from userdb.models import Team, Invitation, TeamMember, UserProfile

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'creator', 'created_at', 'verified')
    list_filter = ('verified',)

    actions = ['verify_and_send_notification_email', 'setup_teams',]

    def verify_and_send_notification_email(self, request, queryset):
        n = 0
        for t in queryset:
            t.verify_and_send_notification_email()
            n += 1
        self.message_user(request, "%s teams were sent notification email" % (n,))

    def setup_teams(self, request, queryset):
        teams = [str(t.pk) for t in queryset]
        return HttpResponseRedirect("/setup/?ids=%s" % (",".join(teams)))

class InvitationAdmin(admin.ModelAdmin):
    list_filter = ('accepted',)

    actions = ['resend_invitation',]

    def resend_invitation(self, request, queryset):
        n = 0
        for i in queryset:
            i.send_invitation(i.made_by)
            n += 1
        self.message_user(request, "%s invitations resent" % (n,))

# Re-register GroupAdmin
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember)
admin.site.register(Invitation, InvitationAdmin)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

