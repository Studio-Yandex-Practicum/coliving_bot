from django.db import models

from profiles.models import UserFromTelegram

from .constants import MatchStatuses, ReportCategories, ReportStatuses


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


class UserReport(models.Model):
    """
    Конфигурация объекта 'UserReport'.
    """

    reporter = models.ForeignKey(
        UserFromTelegram,
        verbose_name="Подавший жалобу",
        null=True,
        on_delete=models.SET_NULL,
        related_name="filed_reports",
    )
    reported_user = models.ForeignKey(
        UserFromTelegram,
        verbose_name="Обвиняемый",
        null=True,
        on_delete=models.SET_NULL,
        related_name="complaints_against",
    )
    text = models.TextField(verbose_name="Текст")
    category = models.TextField(verbose_name="Категория", choices=ReportCategories)
    status = models.TextField(
        verbose_name="Статус",
        choices=ReportStatuses,
        default=ReportStatuses.RECEIVED,
    )
    created_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Жалоба"
        verbose_name_plural = "Жалобы"
        ordering = ("-created_date",)
        constraints = (
            models.UniqueConstraint(
                name="Uniq report",
                fields=("reporter", "reported_user"),
            ),
        )
