from django.urls import path, include
from mails.apps import MailsConfig

app_name = MailsConfig.name

urlpatterns = [
    path("", include("mails.urls", namespace="mails"))
]