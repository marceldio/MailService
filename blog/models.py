from django.db import models

from users.models import User


NULLABLE = {"blank": True, "null": True}


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.CharField(max_length=200, verbose_name="slug", **NULLABLE)
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(
        upload_to="blog/image", **NULLABLE, verbose_name="Изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    view_counter = models.PositiveIntegerField(
        default=0, verbose_name="Счетчик просмотров", editable=False
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Автор",
        help_text="Укажите автора статьи",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
