# backend\accounts\models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from .validators import validate_phone_number, validate_name_only_letters


class UserType(models.IntegerChoices):
    customer = 1, _("customer")
    admin = 2, _("admin")
    superuser = 3, _("superuser")


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("type", UserType.superuser.value)

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    type = models.IntegerField(choices=UserType.choices, default=UserType.customer.value)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    """ This will cause Profile to have no unique id and
    the primary key will be the user_id => profile.pk == user.pk
    """
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE, related_name="profile", primary_key=True,)
 
    first_name = models.CharField(max_length=255, blank=True, default="", validators=[validate_name_only_letters])
    last_name = models.CharField(max_length=255, blank=True, default="", validators=[validate_name_only_letters])

    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[validate_phone_number])

    image = models.ImageField(upload_to="profile/%Y/%m/%d/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} profile"



@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance: User, created: bool, **kwargs):
    if not created:
        return

    # if just customer
    # if instance.type != UserType.customer.value:
    #     return

    Profile.objects.get_or_create(user=instance)