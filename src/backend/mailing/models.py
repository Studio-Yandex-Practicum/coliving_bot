from django.db import models
from django.utils import timezone

from .constants import MailingStatus

TELEGRAM_API_HTML_STYLE_URL = "https://core.telegram.org/bots/api#html-style"


class Mailing(models.Model):
    """
    Модель для работы с рассылками.
    """

    text = models.TextField(
        verbose_name="Текст сообщения",
        help_text=(
            "Здесь можно использовать некоторые теги HTML"
            f' (<a href="{TELEGRAM_API_HTML_STYLE_URL}">'
            f"{TELEGRAM_API_HTML_STYLE_URL}</a>)."
            " Например, <code>&lt;b&gt;жирный текст&lt;/b&gt;</code>."
            " А также вставлять эмодзи 😊."
        ),
        max_length=1024,
    )
    send_date = models.DateTimeField(
        verbose_name="Дата рассылки",
        default=timezone.now,
        help_text=(
            "Наличие рассылки проверяется каждый час, поэтому,"
            " если выставлено 12:34, рассылка начнётся в 13:00."
        ),
    )
    image = models.ImageField(
        upload_to="mailings/",
        null=True,
        blank=True,
        verbose_name="Фото к сообщению",
    )
    status = models.CharField(
        max_length=10,
        choices=MailingStatus,
        default=MailingStatus.WAITING,
        verbose_name="Статус",
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"Сообщение для рассылки {self.id}"
