from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class KnownDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_agent = models.TextField()
    last_seen = models.DateTimeField()