# backend\accounts\api_urls.py
from django.urls import path
from . import api_views


app_name= 'accounts'


urlpatterns = [
    path("register/", api_views.RegisterAPIView.as_view(), name="accounts-register"),
    path("login/", api_views.LoginAPIView.as_view(), name="accounts-login"),
    path("logout/", api_views.LogoutAPIView.as_view(), name="accounts-logout"),
    path("token/refresh/", api_views.TokenRefreshAPIView.as_view(), name="accounts-token-refresh"),

    path("me/", api_views.MeAPIView.as_view(), name="accounts-me"),
    path("password/change/", api_views.ChangePasswordAPIView.as_view(), name="accounts-password-change"),
    path("password/reset/", api_views.PasswordResetRequestAPIView.as_view(), name="accounts-password-reset"),
    path("password/reset/confirm/", api_views.PasswordResetConfirmAPIView.as_view(), name="accounts-password-reset-confirm"),
]
