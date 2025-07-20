from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import UserRegister, CustomTokenObtainPairView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', UserRegister.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]