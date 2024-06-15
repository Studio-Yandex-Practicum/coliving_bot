from django.db import models

from images.utils import images_directory_path
from images.validators import image_size_validator

from .constants import MailingStatus


class Mailing(models.Model):
    """
    Модель для работы с рассылками.
    """

    text = models.TextField(verbose_name="Текст сообщения")
    send_date = models.DateTimeField(verbose_name="Дата рассылки")
    image = models.ImageField(
        upload_to=images_directory_path,
        validators=(image_size_validator,),
        null=True,
        blank=True,
        verbose_name="Фото для рассылки",
    )
    is_sent = models.CharField(
        max_length=20,
        choices=MailingStatus,
        default=MailingStatus.WAITING,
        verbose_name="Отправлено",
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
