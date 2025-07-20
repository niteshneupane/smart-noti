from django.contrib import admin
from .models import KnownDevice
# Register your models here.

class KnownDeviceAdmin(admin.ModelAdmin):
    list_display = ["user", "user_agent", "last_seen"]

admin.site.register(KnownDevice,KnownDeviceAdmin)

