# backend\communications\api_urls.py
from django.urls import path
from .api_views import ContactMessageCreateAPIView, NewsletterSubscribeAPIView

app_name= 'communications'

urlpatterns = [
    path("contact/", ContactMessageCreateAPIView.as_view(), name="contact-create"),
    path("newsletter/subscribe/", NewsletterSubscribeAPIView.as_view(), name="newsletter-subscribe"),
]
