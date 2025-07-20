from django.contrib import admin
from .models import Notification, NotificationPreference, DeliveryStatus

# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "event_type","is_read"]
admin.site.register(Notification,NotificationAdmin)


class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ["user"]
admin.site.register(NotificationPreference,NotificationPreferenceAdmin)


class DeliveryStatusAdmin(admin.ModelAdmin):
    list_display = ["notification","channel","status"]
admin.site.register(DeliveryStatus,DeliveryStatusAdmin)

