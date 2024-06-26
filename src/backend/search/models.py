from django.db import models
from django.utils import timezone

from profiles.models import Coliving, Profile, UserFromTelegram
from search.constants import MatchStatuses, ReportCategories, ReportStatuses


class Like(models.Model):
    status = models.SmallIntegerField(
        verbose_name="Статус запроса",
        choices=MatchStatuses,
        default=MatchStatuses.is_pending,
    )
    match_date = models.DateTimeField(
        verbose_name="Дата ответа",
        null=True,
        blank=True,
    )
    created_date = models.DateTimeField(
        verbose_name="Дата запроса",
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class ProfileLike(Like):
    sender = models.ForeignKey(
        Profile,
        verbose_name="Отправитель",
        on_delete=models.CASCADE,
        related_name="sent_likes",
    )
    receiver = models.ForeignKey(
        Profile,
        verbose_name="Получатель",
        on_delete=models.CASCADE,
        related_name="received_likes",
    )

    class Meta:
        unique_together = ("sender", "receiver")
        constraints = [
            models.CheckConstraint(
                check=~models.Q(sender=models.F("receiver")),
                name="different_sender_receiver",
            ),
        ]


class ColivingLike(Like):
    sender = models.ForeignKey(
        Profile,
        verbose_name="Отправитель",
        on_delete=models.CASCADE,
        related_name="liked_colivings",
    )
    coliving = models.ForeignKey(
        Coliving,
        verbose_name="Комната Coliving",
        on_delete=models.CASCADE,
        related_name="likes",
    )

    class Meta:
        unique_together = ("sender", "coliving")

    def save(self, *args, **kwargs):
        if self.id:
            self.match_date = timezone.now()
        return super().save(*args, **kwargs)


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
    screenshot = models.ImageField(upload_to="user_reports/", null=True)
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

    def __str__(self):
        return f"Жалоба №{self.id}"
