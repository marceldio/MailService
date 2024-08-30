from django.db import models

from users.models import User


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
        ordering = ["first_name", "last_name", "email", "comment"]


class Maill(models.Model):
    """Модель Сообщение"""

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Тело письма")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["title"]


class Sending(models.Model):
    """Модель рассылка"""

    FREQUENCY_CHOICES = [
        ("daily", "daily"),
        ("weekly", "weekly"),
        ("monthly", "monthly"),
    ]

    STATUS_CHOICES = [
        ("created", "created"),
        ("launched", "launched"),
        ("completed", "completed"),
    ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    frequency = models.CharField(
        max_length=15, choices=FREQUENCY_CHOICES, verbose_name="Периодичность"
    )
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, verbose_name="Статус"
    )
    company = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Название компании"
    )
    email = models.ForeignKey(
        Recipient, on_delete=models.CASCADE, verbose_name="Почта Адресата"
    )
    topic = models.ForeignKey(
        Maill, on_delete=models.CASCADE, related_name="Тема", blank=True, null=True
    )
    letter = models.ForeignKey(
        Maill, on_delete=models.CASCADE, related_name="Письмо", blank=True, null=True
    )

    def __str__(self):
        return f"{self.topic}: {self.created_at}, {self.frequency}, {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-created_at"]


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
    title = models.ForeignKey(
        Sending, on_delete=models.CASCADE, verbose_name="Тема рассылки"
    )

    def __str__(self):
        return f"Отправка: {self.event_datetime}"

    class Meta:
        verbose_name = "Отправка"
        verbose_name_plural = "Отправки"
