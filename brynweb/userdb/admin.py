from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect

from userdb.models import Team, Invitation, TeamMember, UserProfile, Region

from scripts.setup_team import setup_tenant


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'creator', 'created_at', 'verified',
                    'tenants_available')
    list_filter = ('verified',)

    actions = ['verify_and_send_notification_email', 'create_warwick_tenant',
               'create_bham_tenant', 'create_cardiff_tenant', 'create_swansea_tenant']

    def verify_and_send_notification_email(self, request, queryset):
        n = 0
        for t in queryset:
            t.verify_and_send_notification_email()
            n += 1
        self.message_user(request,
                          "%s teams were sent notification email" % (n,))

    def create_tenant(self, region, request, queryset):
        n = 0
        for t in queryset:
            try:
                setup_tenant(t, region)
            except Exception as e:
                self.message_user(request,
                                  "Failed to setup tenant %s: %s" % (t, e))
            n += 1
        self.message_user(request, "Created %s tenants" % (n,))

    def create_warwick_tenant(self, request, queryset):
        self.create_tenant(Region.objects.get(name='warwick'),
                           request, queryset)

    def create_bham_tenant(self, request, queryset):
        self.create_tenant(Region.objects.get(name='bham'), request, queryset)

    def create_cardiff_tenant(self, request, queryset):
        self.create_tenant(Region.objects.get(name='cardiff'),
                           request, queryset)

    def create_swansea_tenant(self, request, queryset):
        self.create_tenant(Region.objects.get(name='swansea'),
                           request, queryset)

    def setup_teams(self, request, queryset):
        teams = [str(t.pk) for t in queryset]
        return HttpResponseRedirect("/setup/?ids=%s" % (",".join(teams)))


class InvitationAdmin(admin.ModelAdmin):
    list_filter = ('accepted',)

    actions = ['resend_invitation']

    def resend_invitation(self, request, queryset):
        n = 0
        for i in queryset:
            i.send_invitation(i.made_by)
            n += 1
        self.message_user(request, "%s invitations resent" % (n,))


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    list_filter = ('userprofile__email_validated',)

    actions = ['resend_email_activation_link']

    inlines = (UserProfileInline,)

    def resend_email_activation_link(self, request, queryset):
        for u in queryset:
            u.userprofile.send_validation_link(u)
        self.message_user(request, 'Validation links resent.')


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Region)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
