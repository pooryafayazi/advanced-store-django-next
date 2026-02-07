# backend\communications\admin.py
from django.contrib import admin
from .models import ContactMessage, NewsletterSubscriber


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "id", "email", "subject", "status", "created_date")
    list_filter = ("status", "created_date")
    search_fields = ("full_name", "email", "subject")
    readonly_fields = ("created_date", "updated_date", "ip_address", "user_agent")


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "id", "is_active", "created_date")
    list_filter = ("is_active", "created_date")
    search_fields = ("email",)
    readonly_fields = ("created_date", "updated_date", "unsubscribed_date")