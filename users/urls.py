from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    UserCreateView,
    email_verification,
    UserProfileView,
    reset_password,
)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("reset-password/", reset_password, name="reset_password"),
    path("email-confirm/<str:token>/", email_verification, name="email_confirm"),
]
