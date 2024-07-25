from django.core.exceptions import ValidationError
from django.db import models


class UsefulMaterial(models.Model):
    title = models.CharField(
        max_length=32,
        unique=True,
        verbose_name="Название",
        help_text='Текст кнопки в меню "Полезное".',
    )
    file = models.FileField(
        upload_to="materials/",
        blank=True,
        null=True,
        verbose_name="Файл",
        help_text=(
            "Загрузите файл (например, PDF)."
            " Это поле необязательно, если заполнена ссылка."
        ),
    )
    link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка",
        help_text=(
            "Введите URL-ссылку на материал."
            " Это поле необязательно, если загружен файл."
        ),
    )

    def clean(self):
        if not self.file and not self.link:
            raise ValidationError(
                'Одно из полей "Файл" или "Ссылка" должно быть заполнено.'
            )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Полезный материал"
        verbose_name_plural = "Полезные материалы"
