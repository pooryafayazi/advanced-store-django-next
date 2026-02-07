# backend\accounts\api_urls.py
from django.urls import path
from . import api_views


app_name= 'accounts'


urlpatterns = [
    path("password/reset/", api_views.PasswordResetRequestAPIView.as_view(), name='password-reset'),
    path("password/reset/confirm/", api_views.PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),

]