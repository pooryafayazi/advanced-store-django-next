# backend\communications\api_views.py
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import ContactMessage, NewsletterSubscriber
from .serializers import ContactMessageCreateSerializer, NewsletterSubscribeSerializer


class ContactMessageCreateAPIView(generics.CreateAPIView):
    serializer_class = ContactMessageCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        req = self.request
        user = req.user if req.user.is_authenticated else None
        serializer.save(user=user, ip_address=req.META.get("REMOTE_ADDR"), user_agent=req.META.get("HTTP_USER_AGENT", ""),)


class NewsletterSubscribeAPIView(generics.GenericAPIView):
    serializer_class = NewsletterSubscribeSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"].lower()

        obj, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if not created and obj.is_active:
            return Response({"detail": "Already subscribed."}, status=status.HTTP_200_OK)
        
        obj.is_active= True
        obj.unsubscribed_date = None
        obj.save(update_fields=["is_active", "unsubscribed_date", "updated_date"])
        return Response({"detail": "Subscribed."}, status=status.HTTP_201_CREATED)