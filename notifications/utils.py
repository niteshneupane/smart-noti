
from .models import ALL_CHANNEL_KEYS, Notification, DeliveryStatus, NotificationPreference
from django.core.mail import send_mail

def dispatch_notification(user, title, body, event_type):
    try:
        prefs = NotificationPreference.objects.get(user=user)

        if event_type == 'login':
            channels = ALL_CHANNEL_KEYS
        else:
            channels = getattr(prefs, event_type, [])

        Notification.objects.create(
            user=user,
            title=title,
            body=body,
            event_type=event_type
        )

        for channel in channels:
            if channel == "in_app":
                send_fcm()
            elif channel == "email":
                send_email(title,body,user.email)
            elif channel == "sms":
                send_sms() 
            else:
                print(f"channel doesnt exists {channel}")
    except Exception as e:
        print(f"Does not existsssssss {e}")


def send_email(subject,body,to):
    try:
        send_mail(
            subject,
            body,
            "admin@smartnoti.com",
            [to],
        )
    except Exception as e:
        print(f"EMAIL FAILED {e}")

def send_fcm():
    try:

        print("FCM Sending")
    except Exception as e:
        print(f"FCM FAILED {e}")

def send_sms():
    try:
        print("Sendingggggg sms")

    except Exception as e:
        print(f"SMS FAILED {e}")