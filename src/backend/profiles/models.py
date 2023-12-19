from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models

from .constants import ColivingTypes, GenderRoles, Literals, Restrictions


class Location(models.Model):
    """
    Конфигурация объекта 'Location'.
    """

    name = models.TextField(
        verbose_name="Название",
    )

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"
        ordering = ("name",)

    def __str__(self):
        return self.name


class UserFromTelegram(models.Model):
    """
    Конфигурация объекта 'UserFromTelegram'.
    """

    telegram_id = models.PositiveIntegerField(
        verbose_name="Идентификатор пользователя Telegram",
        unique=True,
        db_index=True,
    )
    residence = models.ForeignKey(
        "Coliving",
        verbose_name="Проживает в коливинге",
        on_delete=models.SET_NULL,
        related_name="roommates",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("telegram_id",)

    def __str__(self):
        return f"Пользователь (Telegram id: {self.telegram_id})"


class BaseProfileColiving(models.Model):
    """
    Общие атрибуты объектов 'Profile' и 'Coliving'.
    """

    location = models.ForeignKey(
        Location,
        verbose_name="Местоположение",
        on_delete=models.CASCADE,
    )
    about = models.TextField(
        verbose_name="Описание",
        max_length=Restrictions.ABOUT_TEST_MAX,
        blank=True,
        null=True,
    )
    is_visible = models.BooleanField(
        verbose_name="Отображать при поиске",
        default=True,
    )
    viewers = models.ManyToManyField(
        UserFromTelegram,
        verbose_name="Просмотры",
        blank=True,
    )
    created_date = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        default_related_name = "%(class)s"


class Profile(BaseProfileColiving):
    """
    Конфигурация объекта 'Profile'.
    """

    user = models.OneToOneField(
        UserFromTelegram,
        verbose_name="Пользователь Telegram",
        on_delete=models.CASCADE,
        related_name="user_profile",
    )
    name = models.TextField(
        verbose_name="Имя пользователя",
        validators=(
            MinLengthValidator(Restrictions.PROFILE_NAME_MIN),
            MaxLengthValidator(Restrictions.PROFILE_NAME_MAX),
            RegexValidator(
                regex=Literals.NAME_CHECK,
                message=Literals.NAME_CHECK_MESSAGE,
            ),
        ),
    )
    sex = models.TextField(
        verbose_name="Пол",
        choices=GenderRoles,
    )
    age = models.PositiveSmallIntegerField(
        verbose_name="Возраст",
        validators=(
            MinValueValidator(Restrictions.AGE_MIN),
            MaxValueValidator(Restrictions.AGE_MAX),
        ),
    )

    class Meta(BaseProfileColiving.Meta):
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        ordering = ("name", "sex", "location")

    def __str__(self):
        return f"Профиль: {self.name[:Restrictions.PROFILE_NAME_STR]}, {self.user}"


class Coliving(BaseProfileColiving):
    """
    Конфигурация объекта 'Coliving'.
    """

    host = models.ForeignKey(
        UserFromTelegram,
        verbose_name="Создатель коливинга",
        related_name="colivings",
        on_delete=models.CASCADE,
    )
    price = models.PositiveIntegerField(
        verbose_name="Цена",
        validators=(
            MinValueValidator(Restrictions.PRICE_MIN),
            MaxValueValidator(Restrictions.PRICE_MAX),
        ),
    )
    room_type = models.TextField(
        verbose_name="Тип коливинга",
        choices=ColivingTypes,
    )

    class Meta(BaseProfileColiving.Meta):
        verbose_name = "Коливинг"
        verbose_name_plural = "Коливинги"
        ordering = ("room_type",)

    def __str__(self):
        return f"Коливинг {self.location}"
