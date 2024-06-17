from django.db import models


class MailingStatus(models.TextChoices):
    WAITING = ("is_waiting", "Ждёт")
    SENDING = ("is_sending", "Отправляется")
    SENT = ("is_sent", "Отправлено")
