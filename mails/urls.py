from django.urls import path
from mails.apps import MailsConfig
from mails.views import (
    RecipientListView, RecipientDetailView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView,
    SendingListView, SendingDeleteView, SendingCreateView, SendingDetailView, SendingUpdateView,
    MaillListView, MaillDetailView, MaillCreateView, MaillUpdateView, MaillDeleteView,
    home,
    contact,
    about,
)

app_name = MailsConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("recipient_list", RecipientListView.as_view(), name="recipient_list"),
    path(
        "recipient_view/<int:pk>/", RecipientDetailView.as_view(), name="recipient_view"
    ),
    path("recipient_create/", RecipientCreateView.as_view(), name="recipient_create"),
    path(
        "recipient_update/<int:pk>/",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient_delete<int:pk>/",
        RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),

    path("sending_list/", SendingListView.as_view(), name="sending_list"),
    path("sending_create/", SendingCreateView.as_view(), name="sending_create"),
    path(
        "sending_delete/<int:pk>/", SendingDeleteView.as_view(), name="sending_delete"
    ),
    path("sending_update/<int:pk>/", SendingUpdateView.as_view(), name="sending_update"),
    path("sending_detail/<int:pk>/", SendingDetailView.as_view(), name="sending_detail"),

    path("maill_list/", MaillListView.as_view(), name="maill_list"),
    path("maill_create/", MaillCreateView.as_view(), name="maill_create"),
    path("maill_delete/<int:pk>/", MaillDeleteView.as_view(), name="maill_delete"),
    path("maill_update/<int:pk>/", MaillUpdateView.as_view(), name="maill_update"),
    path("maill_detail/<int:pk>/", MaillDetailView.as_view(), name="maill_detail"),

    path("contact/", contact, name="contact"),
    path("about/", about, name="about"),
]
