from django.urls import path
from mails.apps import MailsConfig
from mails.views import home

app_name = MailsConfig.name

urlpatterns = [path("", home, name="home")]
