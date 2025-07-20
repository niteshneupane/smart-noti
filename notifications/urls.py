from django.urls import path
from .views import UnreadNotifications,ReadNotifications,NotificationHistory,PreferencesView, NotificationTrigger

urlpatterns = [
    path('unread/',UnreadNotifications.as_view(),name='unread_notification'),
    path('read/',ReadNotifications.as_view(),name='read_notification' ),
    path('history/',NotificationHistory.as_view(),name='notification_history' ),
    path('preferences/', PreferencesView.as_view(),name='preferences'),
    path('trigger/',NotificationTrigger.as_view(),name='trigger',),
]