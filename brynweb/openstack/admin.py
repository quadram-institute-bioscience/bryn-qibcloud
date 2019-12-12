from django.contrib import admin
from .models import Tenant, RegionSettings, ActionLog, HypervisorStats

class TenantAdmin(admin.ModelAdmin):
    pass

class ActionLogAdmin(admin.ModelAdmin):
    list_filter = ('error',)

admin.site.register(Tenant, TenantAdmin)
admin.site.register(RegionSettings)
admin.site.register(ActionLog, ActionLogAdmin)
admin.site.register(HypervisorStats)
