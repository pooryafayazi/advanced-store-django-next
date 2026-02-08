# backend\accounts\api_views.py
import threading
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    TokenRefreshSerializer,
    RegisterSerializer,
    UserMeSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)

User = get_user_model()
token_generator = PasswordResetTokenGenerator()
logger = logging.getLogger(__name__)


def _send_reset_email_async(subject: str, message: str, to_email: str):
    """
    Threaded send_mail (no celery).
    """
    t = threading.Thread(
        target=send_mail,
        kwargs=dict(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[to_email], fail_silently=False,),
        daemon=True,)
    t.start()


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh), "user": UserMeSerializer(user).data,}, status=status.HTTP_200_OK)


class TokenRefreshAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, requset):
        ser = TokenRefreshSerializer(data=requset.data)
        ser.is_valid(raise_exception=True)

        refresh = RefreshToken(ser.validated_data["refresh"])
        return Response({"access": str(refresh.access_token)}, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = LogoutSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        try:
            token = RefreshToken(ser.validated_data["refresh"])
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        
        # return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Logged out successfully."}, status=200)


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response({"detail": "Registered successfully."}, status=status.HTTP_201_CREATED)


class MeAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserMeSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = ChangePasswordSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(ser.validated_data["old_password"]):
            return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(ser.validated_data["new_password1"])
        user.save(update_fields=["password"])
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)


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
            message = f"Use this link to reset your password:\n{reset_link}\n(This link expires in 48 hours.)"
            _send_reset_email_async(subject, message, user.email)

        return Response({"detail": "If an account exists for this email, a reset link has been sent."}, status=status.HTTP_200_OK,)


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
