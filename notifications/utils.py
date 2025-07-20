
from .models import ALL_CHANNEL_KEYS, Notification, DeliveryStatus, NotificationPreference
from django.core.mail import send_mail

def dispatch_notification(user, title, body, event_type):
    try:
        prefs = NotificationPreference.objects.get(user=user)

        if event_type == 'login':
            channels = ALL_CHANNEL_KEYS
        else:
            channels = getattr(prefs, event_type, [])

        noti = Notification.objects.create(
            user=user,
            title=title,
            body=body,
            event_type=event_type
        )

        for channel in channels:
            if channel == "in_app":
                send_fcm(noti)
            elif channel == "email":
                send_email(title,body,user.email,noti)
            elif channel == "sms":
                send_sms(noti) 
            else:
                print(f"channel doesnt exists {channel}")
    except Exception as e:
        print(f"Does not existsssssss {e}")


def send_email(subject,body,to,noti):
    try:
        dd = send_mail(
            subject,
            body,
            "admin@smartnoti.com",
            [to],
        )
        print(f"DD {dd}")
        create_delivery_status(noti,"email","failed")

    except Exception as e:
        print(f"EMAIL FAILED {e}")
        create_delivery_status(noti,"email","failed")


def send_fcm(noti):
    try:
        # TODO: implement fcm
        create_delivery_status(noti,"in_app","sent")


        print("FCM Sending")
    except Exception as e:
        print(f"FCM FAILED {e}")
        create_delivery_status(noti,"in_app","failed")


def send_sms(noti):
    try:
        # TODO: implement sms

        print("Sendingggggg sms")
        create_delivery_status(noti,"sms","sent")


    except Exception as e:
        print(f"SMS FAILED {e}")
        create_delivery_status(noti,"sms","failed")


def create_delivery_status(noti,channel,status):
    try:
        DeliveryStatus.objects.create(
            notification=noti,
            channel=channel,
            status=status
        )
    except Exception as e:
        print(f"exception {e}")