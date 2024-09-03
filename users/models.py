from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    company = models.CharField(max_length=100, verbose_name="Название компании")
    avatar = models.ImageField(
        upload_to="users/", blank=True, null=True, verbose_name="Аватар"
    )
    phone = models.CharField(
        max_length=35, blank=True, null=True, verbose_name="Телефон"
    )
    country = models.CharField(
        max_length=35, blank=True, null=True, verbose_name="Страна"
    )
    is_active = models.BooleanField(default=False, verbose_name="Активный")
    token = models.CharField(
        max_length=255, verbose_name="Токен", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["company"]
        permissions = [
            ("can_block_users", "Can block users"),
            ("can_view_users", "Can view users"),
        ]
