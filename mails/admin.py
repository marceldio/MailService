from django.contrib import admin
from mails.models import Maill, Recipient


@admin.register(Maill)
class MaillAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "sent", "created_at", "updated_at")
    list_filter = (
        "title",
        "recipient",
        "sent",
    )
    list_search = (
        "id",
        "title",
        "recipient",
    )


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email")
    list_filter = (
        "email", "comment",
    )
    list_search = (
        "email", 'comment',
    )
