import random
import secrets
import string
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save(update_fields=["token", "is_active"])
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"

        send_mail(
            subject="Подтверждение регистрации",
            message=f"Перейдите по ссылке для подтверждения регистрации {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def generate_random_password(length=10):
    # Генерация случайного пароля из букв и цифр
    characters = string.ascii_letters + string.digits

    return "".join(random.choice(characters) for _ in range(length))


def reset_password(request):
    # context = {
    #     'success_message': 'Пароль успешно сброшен на email'
    # }
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = get_object_or_404(User, email=email)
            new_password = generate_random_password()
            user.password = make_password(new_password)
            user.save()
            # Отправка письма с новым паролем
            send_mail(
                "Восстановление пароля",
                f"Ваш новый пароль: {new_password}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,  # Отключение отправки ошибок
            )
            return HttpResponse("Пароль сброшен на email")
        except User.DoesNotExist:
            return HttpResponse("Пользователь с таким email не найден")


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("mails:home")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)
