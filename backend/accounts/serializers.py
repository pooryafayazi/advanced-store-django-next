# backend\accounts\serializers.py
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import serializers

from .models import Profile

User = get_user_model()
token_generator = PasswordResetTokenGenerator()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError({"detail": "Invalid credentials."})
        if not user.is_active:
            raise serializers.ValidationError({"detail": "User is inactive."})
        attrs["user"] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "phone_number", "image", "description", "created_date", "updated_date")
        read_only_fields = ("created_date", "updated_date")


class UserMeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "email", "type", "is_active", "is_verified", "created_date", "updated_date", "profile")
        read_only_fields = ("id", "email", "type", "is_active", "is_verified", "created_date", "updated_date")

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)
        if profile_data is not None:
            prof = instance.profile
            for k, v in profile_data.items():
                setattr(prof, k, v)
            prof.save()
        return instance


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        validate_password(attrs["password1"])
        return attrs

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password1"]

        user = User.objects.create_user(
            email=email,
            password=password,
        )

        prof = user.profile
        prof.first_name = validated_data["first_name"]
        prof.last_name = validated_data["last_name"]
        prof.phone_number = validated_data.get("phone_number") or ""
        prof.save()

        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password1"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password2": "Passwords do not match."})
        validate_password(attrs["new_password1"])
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password2": "Passwords do not match."})
        validate_password(attrs["new_password"])
        return attrs
