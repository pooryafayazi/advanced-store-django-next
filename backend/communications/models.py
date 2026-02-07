# backend\communications\models.py
from django.db import models
from django.conf import settings


class TimeStampeModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class ContactMessage(TimeStampeModel):
    class Status(models.TextChoices):
        NEW = "new" , "New"
        READ = "read" , "Read"
        ARCHIVED = "archived" , "Archived"
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="contact_messages")
    full_name = models.CharField(max_length=127)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, default="")
    subject = models.CharField(max_length=200)
    message = models.TextField()

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.full_name} - {self.subject}"


class NewsletterSubscriber(TimeStampeModel):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    unsubscribed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email


