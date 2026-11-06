
from django.contrib import admin
from .models import ContactEnquiry


@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "service", "budget", "created_at")
    list_filter = ("service", "created_at")
    search_fields = ("name", "phone", "email")
    readonly_fields = ("created_at",)
