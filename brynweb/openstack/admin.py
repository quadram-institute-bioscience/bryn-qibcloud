from django.contrib import admin
from models import Tenant, RegionSettings

class TenantAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tenant, TenantAdmin)
admin.site.register(RegionSettings)

