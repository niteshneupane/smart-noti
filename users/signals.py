from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import NotificationPreference
from notifications.utils import dispatch_notification

@receiver(post_save, sender=User)
def on_user_created(sender, instance, created, **kwargs):
    if created:
        print(f"Signal received for new user: {instance.email}")
        NotificationPreference.objects.get_or_create(
            user=instance,
        )

        dispatch_notification(
            user=instance,
            title="Welcome to the Smart System!",
            body="Thanks for registering",
            event_type='login'
        )