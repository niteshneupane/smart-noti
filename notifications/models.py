from django.contrib.auth.models import User
from django.db import models
from multiselectfield import MultiSelectField
# Create your models here.

CHANNEL_CHOICES = [('in_app', 'In-App'), ('email', 'Email'), ('sms', 'SMS')]
ALL_CHANNEL_KEYS = [choice[0] for choice in CHANNEL_CHOICES]

EVENT_TYPES = [('comment', 'New Comment'),('login', 'Login'), ('unrecog_login', 'Unrecognized Login'), ('summary', 'Weekly Summary')]

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    event_type = models.CharField(choices=EVENT_TYPES, max_length=20)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + ", " + self.user.email

class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comment = MultiSelectField(choices=CHANNEL_CHOICES,default=ALL_CHANNEL_KEYS)
    unauthorized_login = MultiSelectField(choices=CHANNEL_CHOICES,default=ALL_CHANNEL_KEYS)
    summary = MultiSelectField(choices=CHANNEL_CHOICES,default=ALL_CHANNEL_KEYS)

class DeliveryStatus(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    channel = models.CharField(choices=CHANNEL_CHOICES, max_length=20)
    status = models.CharField(max_length=10, choices=[('sent', 'Sent'), ('failed', 'Failed')])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Delivery Status"
