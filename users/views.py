import random
import secrets
import string
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm, UserProfileManagerForm
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
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            new_password = generate_random_password()
            user.password = make_password(new_password)
            user.save()

            # Отправка письма с новым паролем
            send_mail(
                "Восстановление пароля",
                f"Ваш новый пароль: {new_password}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            success_message = "Пароль сброшен на ваш email."
        else:
            success_message = "Пользователь с таким email не найден."

        return render(
            request, "users/reset_password.html", {"success_massage": success_message}
        )

    # Если метод не POST, рендерим страницу сброса пароля (GET запрос)
    return render(request, "users/reset_password.html")


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:user_list")

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        if pk:
            return get_object_or_404(User, pk=pk)
        raise Http404("User not found")

    def get_form_class(self):
        user = self.request.user
        if user == self.get_object():
            return UserProfileForm
        if user.has_perm("users.can_block_users"):
            return UserProfileManagerForm
        raise PermissionDenied


# class UserProfileView(UpdateView):
#     model = User
#     success_url = reverse_lazy("users:user_list")
#
#     def get_object(self, queryset=None):
#         user = self.request.user
#         if user.has_perm("users.can_block_users"):
#             # Если менеджер, получаем пользователя по ID из URL
#             user_pk = self.kwargs.get("pk")
#             if user_pk:
#                 return get_object_or_404(User, pk=user_pk)
#         # Если не менеджер или не указан ID, возвращаем текущего пользователя
#         return user
#
#     def get_form_class(self):
#         user = self.request.user
#         if user == self.get_object():
#             # Если пользователь редактирует сам себя, используем обычную форму
#             return UserProfileForm
#         if user.has_perm("users.can_block_users"):
#             # Если менеджер редактирует другого пользователя, используем форму для менеджера
#             return UserProfileManagerForm
#         raise PermissionDenied
#
#     def form_valid(self, form):
#         # Проверка на попытку менеджера деактивировать самого себя
#         if self.object == self.request.user and not form.cleaned_data.get('is_active', True):
#             form.add_error(None, "Вы не можете деактивировать самого себя.")
#             return self.form_invalid(form)
#
#         form.save()
#         return redirect(self.success_url)


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"

    def get_queryset(self, *args, **kwargs):
        # queryset = super().get_queryset()
        queryset = User.objects.all()
        return queryset
