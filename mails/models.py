from django.db import models
from users.models import User
from django.utils import timezone
from datetime import timedelta


class Recipient(models.Model):
    """Модель Адресат"""

    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(
        max_length=100, verbose_name="Имя", blank=True, null=True
    )
    last_name = models.CharField(
        max_length=100, verbose_name="Фамилия", blank=True, null=True
    )
    middle_name = models.CharField(
        max_length=100, verbose_name="Отчество", blank=True, null=True
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    owner = models.ForeignKey(
        User, verbose_name="Владелец",
        blank=True, null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        if self.first_name:
            if not self.middle_name or self.last_name:
                if not self.middle_name:
                    return f"{self.first_name} {self.last_name}: {self.email}"
                elif not self.last_name:
                    return f"{self.first_name} {self.middle_name}: {self.email}"
                else:
                    return f"{self.first_name}: {self.email}"
            else:
                return f"{self.first_name} {self.middle_name} {self.last_name}: {self.email}"
        else:
            return self.email

    class Meta:
        verbose_name = "Адресат"
        verbose_name_plural = "Адресаты"
        ordering = ["email", "comment"]


class Maill(models.Model):
    """Модель Сообщение"""

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Тело письма")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, verbose_name="Автор",
        blank=True, null=True,
        on_delete=models.SET_NULL
    )


    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["title"]
        permissions = [
            ("can_view_maill", "Can view maill"),
        ]


class Sending(models.Model):
    """Модель рассылка"""

    FREQUENCY_CHOICES = [
        ("daily", "Раз в день"),
        ("weekly", "Раз в неделю"),
        ("monthly", "Раз в месяц"),
    ]

    STATUS_CHOICES = [
        ("created", "Создана"),
        ("launched", "Запущена"),
        ("completed", "Завершена"),
    ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    frequency = models.CharField(
        max_length=15, choices=FREQUENCY_CHOICES, verbose_name="Периодичность"
    )
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, verbose_name="Статус"
    )
    company = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sendings"
    )
    topic = models.ForeignKey(
        Maill, on_delete=models.CASCADE, related_name="Тема", blank=True, null=True
    )
    letter = models.ForeignKey(
        Maill, on_delete=models.CASCADE, related_name="Письмо", blank=True, null=True
    )
    recipients = models.ManyToManyField(Recipient, related_name='sendings')
    scheduled_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Автоматическое присвоение компании из текущего пользователя
        if not self.company_id and 'user' in kwargs:
            self.company = kwargs.pop('user').company

        if not self.scheduled_at:
            if self.frequency == "daily":
                self.scheduled_at = timezone.now() + timedelta(days=1)
            elif self.frequency == "weekly":
                self.scheduled_at = timezone.now() + timedelta(weeks=1)
            elif self.frequency == "monthly":
                self.scheduled_at = timezone.now() + timedelta(days=30)

        super(Sending, self).save(*args, **kwargs)

    def __str__(self):
        return f'Sending {self.id} - {self.status}'


    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-created_at"]
        permissions = [
            ("can_view_sending", "Can view sending"),
        ]


class Event(models.Model):
    """Модель попыток рассылки"""

    EVENT_STATUS_CHOICES = [
        ("failed", "Failed"),
        ("succeeded", "Succeeded"),
    ]
    event_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Отправка")
    event_status = models.CharField(
        max_length=15, choices=EVENT_STATUS_CHOICES, verbose_name="Статус"
    )
    server_response = models.TextField(
        blank=True, null=True, verbose_name="Ответ сервера"
    )
    email = models.ForeignKey(Recipient, on_delete=models.CASCADE, verbose_name="Email")
    topic = models.ForeignKey(
        Sending, on_delete=models.CASCADE, verbose_name="Тема рассылки"
    )

    def __str__(self):
        return f"Отправка: {self.event_datetime}"

    class Meta:
        verbose_name = "Отправка"
        verbose_name_plural = "Отправки"
