from django.contrib import admin
from .models import Login, Message


@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ("login", "password")
    search_fields = ("login",)
    list_per_page = 20


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("theme", "owner", "send_date", "receipt_date")
    list_filter = ("send_date", "receipt_date")
    search_fields = ("theme", "owner__login")
    date_hierarchy = "send_date"
    list_per_page = 20
