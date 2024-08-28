from django.db import models


class Maill(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Содержание")
    recipient = models.EmailField(verbose_name="Адресат")
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["title", "recipient", "updated_at", "created_at", "sent"]


class Recipient(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(
        max_length=100, verbose_name="Фамилия", blank=True, null=True
    )
    middle_name = models.CharField(
        max_length=100, verbose_name="Отчество", blank=True, null=True
    )
    email = models.EmailField(verbose_name="Email")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    maill = models.ForeignKey(
        Maill,
        on_delete=models.SET_NULL,
        verbose_name="Письмо",
        blank=True,
        null=True,
        related_name="maills",
    )

    def __str__(self):
        if not self.middle_name and self.last_name:
            if not self.middle_name:
                return f"{self.first_name} {self.last_name}: {self.email}"
            elif not self.last_name:
                return f"{self.first_name} {self.middle_name}: {self.email}"
        else:
            return (
                f"{self.first_name} {self.middle_name} {self.last_name}: {self.email}"
            )

    class Meta:
        verbose_name = "Адресат"
        verbose_name_plural = "Адресаты"
        ordering = ["first_name", "last_name", "email", "comment"]
