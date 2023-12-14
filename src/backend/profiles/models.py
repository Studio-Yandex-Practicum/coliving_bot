from django.db import models
from django.core.validators import (
    MinValueValidator, MaxValueValidator, MaxLengthValidator,
    MinLengthValidator, RegexValidator,
)

from .constants import Restrictions, ColivingTypes, GenderRoles


class UserFromTelegram(models.Model):
    """
        Объект 'UserFromTelegram'.
    """

    telegram_id = models.PositiveIntegerField(
        verbose_name='Идентификатор пользователя Telegram',
    )
    residence = models.ForeignKey(
        'Coliving',
        verbose_name='Соседи',
        on_delete=models.CASCADE,
        related_name='rommates',
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.telegram_id)


class Location(models.Model):
    """
        Объект 'Location'.
    """

    name = models.TextField(
        verbose_name='Название',
        validators=(
            MinLengthValidator(Restrictions.LOCATION_NAME_MIN),
            MaxLengthValidator(Restrictions.LOCATION_NAME_MAX),
            RegexValidator(regex=r'^[А-Яа-яA-Za-z\s]+$'),
        )
    )

    class Meta:

        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class BaseProfileColiving(models.Model):
    """
        Общие атрибуты объектов 'Profile' и 'Coliving'.
    """

    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.CASCADE,
    )
    about = models.TextField(
        verbose_name='Описание',
        max_length=Restrictions.ABOUT_TEXT,
    )
    is_visible = models.BooleanField(
        verbose_name='Видимость',
    )
    viewers = models.ManyToManyField(
        UserFromTelegram,
        verbose_name='Зрители',
    )
    created_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    class Meta:

        abstract = True
        default_related_name = '%(class)s'


class Profile(BaseProfileColiving):
    """
        Объект 'Profile'.
    """

    user = models.OneToOneField(
        UserFromTelegram,
        verbose_name='Пользователь Telegram',
        on_delete=models.CASCADE,
        related_name='user_profile',
    )
    name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=Restrictions.PROFILE_NAME,
    )
    sex = models.TextField(
        verbose_name='Пол',
        choices=GenderRoles,
    )
    age = models.PositiveSmallIntegerField(
        verbose_name='Возраст',
        validators=(
            MinValueValidator(Restrictions.AGE_MIN),
            MaxValueValidator(Restrictions.AGE_MAX),
        )
    )

    class Meta(BaseProfileColiving.Meta):

        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Coliving(BaseProfileColiving):
    """
        Объект 'Coliving'.
    """

    host = models.ForeignKey(
        UserFromTelegram,
        verbose_name='Создатель коливинга',
        related_name='colivings',
        on_delete=models.CASCADE,
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
        validators=(
            MinValueValidator(Restrictions.PRICE_MIN),
            MaxValueValidator(Restrictions.PRICE_MAX),
        )
    )
    room_type = models.TextField(
        verbose_name='Тип коливинга',
        choices=ColivingTypes,
    )

    class Meta(BaseProfileColiving.Meta):

        verbose_name = 'Коливинг'
        verbose_name_plural = 'Коливинги'
