from django.urls import path
from mails.apps import MailsConfig
from mails.views import MaillDetailView, MaillListView, MaillCreateView, MaillUpdateView, MaillDeleteView

app_name = MailsConfig.name

urlpatterns = [
    path("", MaillListView.as_view(), name="maill_list"),
    path("mails/<int:pk>/", MaillDetailView.as_view(), name="maill_detail"),
    path("mails/create", MaillCreateView.as_view(), name="maill_create"),
    path("mails/<int:pk>/update", MaillUpdateView.as_view(), name="maill_update"),
    path("mails/<int:pk>/delete", MaillDeleteView.as_view(), name="maill_delete")
]
