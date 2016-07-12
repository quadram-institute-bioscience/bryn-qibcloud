from django.contrib import admin
from models import Tenant

class TenantAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tenant, TenantAdmin)
