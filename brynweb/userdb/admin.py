from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group

from userdb.models import GroupProfile

class GroupProfileInline(admin.StackedInline):
    model = GroupProfile
    can_delete = False
    verbose_name_plural = 'group'

# Define a new Group admin
class GroupAdmin(BaseGroupAdmin):
    inlines = (GroupProfileInline, )

# Re-register GroupAdmin
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
