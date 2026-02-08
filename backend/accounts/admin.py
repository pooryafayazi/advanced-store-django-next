
# backend\accounts\admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User, Profile
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    model = User
    ordering = ("-created_date",)
    list_display = ("id", "email", "type", "is_active", "is_staff", "is_verified", "created_date")
    list_filter = ("type", "is_active", "is_staff", "is_verified")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_verified", "type", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_date", "updated_date")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_active", "is_staff", "is_verified", "type"),
        }),
    )

    search_fields = ("email",)
    readonly_fields = ("created_date", "updated_date")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user_id", "user", "first_name", "last_name", "phone_number", "updated_date")
    search_fields = ("user__email", "first_name", "last_name", "phone_number")
    readonly_fields = ("created_date", "updated_date")
