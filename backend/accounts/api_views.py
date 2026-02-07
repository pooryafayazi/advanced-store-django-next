# backend\accounts\api_views.py
import threading
import logging

logger = logging.getLogger(__name__)

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PasswordResetConfirmSerializer, PasswordResetRequestSerializer

User = get_user_model()
token_generator = PasswordResetTokenGenerator()


def _send_reset_email_async(subject: str, message: str, to_email: str):
    t = threading.Thread(target=send_mail,
                         kwargs=dict(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[to_email], fail_silently=True),
                         daemon=True)
    t.start()


class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = PasswordResetRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"]

        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            reset_link = f"{settings.FRONTEND_BASE_URL}/reset-password?uid={uid}&token={token}"
            if settings.DEBUG:
                logger.warning("DEV reset link: %s", reset_link)

            subject = "Reset your password"
            message = f"Use this link to reset your password (valid for 48 hours): \n{reset_link}"

            _send_reset_email_async(subject, message, user.email)

        return Response(
            {"detail": "If an account exists for this email, a reset link has been sent."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = PasswordResetConfirmSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        uid = ser.validated_data["uid"]
        token = ser.validated_data["token"]
        new_password = ser.validated_data["new_password"]

        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id, is_active=True)
        except Exception:
            return Response({"detail": "Invalid link."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not token_generator.check_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save(update_fields=["password"])

        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)