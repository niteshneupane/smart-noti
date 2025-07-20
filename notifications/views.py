from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Notification, NotificationPreference
from .serializers import NotificationSerializer, ReadNotificationSerializer, NotificationPreferenceSerializer, TriggerEventSerializer
from .utils import dispatch_notification
# Create your views here.


class UnreadNotifications(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifs = Notification.objects.filter(user=request.user, is_read=False)
        return Response(NotificationSerializer(notifs, many=True).data)

class ReadNotifications(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = ReadNotificationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            noti =  Notification.objects.get(id=serializer.validated_data['id'], user=request.user)
            print(noti)
            if not noti.is_read:
                noti.is_read = True
                noti.save()
                return Response({"message": "marked as read"})
            return Response({"message": "Notification has already been read"})
        except Notification.DoesNotExist:
            return Response({"message":"Not found"},status=HTTP_404_NOT_FOUND)
        
        

class NotificationHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifs = Notification.objects.filter(user=request.user).order_by('-timestamp')
        return Response(NotificationSerializer(notifs, many=True).data)

class PreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        prefs, _ = NotificationPreference.objects.get_or_create(user=request.user)
        return Response(NotificationPreferenceSerializer(prefs).data)

    def post(self, request):
        prefs, _ = NotificationPreference.objects.get_or_create(user=request.user)
        serializer = NotificationPreferenceSerializer(prefs, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class NotificationTrigger(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = TriggerEventSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            event = serializer.validated_data['event_type']
            payload = serializer.validated_data['payload']
            dispatch_notification(user=request.user, title=f"{event} Alert", body=str(payload), event_type=event),
            return Response({"message": "notifications dispatched"}, status=HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=HTTP_400_BAD_REQUEST)

    