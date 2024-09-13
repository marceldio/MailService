from django.contrib import admin
from mails.models import Maill, Recipient, Sending, Event


@admin.register(Maill)
class MaillAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author")
    list_filter = ("title",)
    list_search = (
        "id",
        "title",
    )


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "comment", "owner")
    list_filter = (
        "email",
        "comment",
    )
    list_search = (
        "email",
        "comment",
    )


@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    list_display = ["id", "letter", "scheduled_at", "status", "company"]
    filter_horizontal = ["recipient"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "event_datetime",
        "event_status",
        "server_response",
        "email",
        "topic",
    )
