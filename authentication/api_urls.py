from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .api_views import RegisterAPIView, LoginAPIView, LogoutAPIView, ProfileAPIView, ChangePasswordAPIView

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='api_register'),
    path('auth/login/', LoginAPIView.as_view(), name='api_login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('auth/profile/', ProfileAPIView.as_view(), name='api_profile'),
    path('auth/change-password/', ChangePasswordAPIView.as_view(), name='api_change_password'),
]
