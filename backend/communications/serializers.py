# backend\communications\serializers.py
from rest_framework import serializers
from .models import ContactMessage, NewsletterSubscriber


class ContactMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ("full_name", "email", "phone", "subject", "message")


class NewsletterSubscribeSerializer(serializers.Serializer):
    email = serializers.EmailField()