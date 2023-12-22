from django.db import models

from profiles.models import UserFromTelegram

from .constants import MatchStatuses


class MatchRequest(models.Model):
    """
    Конфигурация объекта 'MatchRequests'.
    """

    sender = models.ForeignKey(
        UserFromTelegram,
        verbose_name="Отправитель",
        on_delete=models.CASCADE,
        related_name="likes",
    )
    receiver = models.ForeignKey(
        UserFromTelegram,
        verbose_name="Получатель",
        on_delete=models.CASCADE,
        related_name="match_requests",
    )
    status = models.SmallIntegerField(
        verbose_name="Статус запроса",
        choices=MatchStatuses,
        default=MatchStatuses.is_pending,
    )
    created_date = models.DateTimeField(
        verbose_name="Дата запроса",
        auto_now_add=True,
    )
    match_date = models.DateTimeField(
        verbose_name="Дата ответа",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Связь"
        verbose_name_plural = "Связи"
        ordering = ("sender", "receiver", "-created_date")
        constraints = (
            models.CheckConstraint(
                check=~models.Q(sender=models.F("receiver")),
                name="Cant match to myself",
            ),
            models.UniqueConstraint(
                name="Uniq match request",
                fields=("sender", "receiver"),
            ),
        )
