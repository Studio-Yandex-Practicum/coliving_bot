from django.db import models
from django.core.validators import (
    MinValueValidator, MaxValueValidator, MaxLengthValidator,
)

from .constants import (
    IntegerRestrictions, ColivingTypes, GenderRoles, Messages,
)


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
    )


class Location(models.Model):
    """
        Объект 'Location'.
    """

    name = models.CharField(
        verbose_name='Имя',
        max_length=IntegerRestrictions.LOCATION_NAME,
        validators=(
            MaxLengthValidator(
                IntegerRestrictions.LOCATION_NAME,
                message=Messages.LOCATION_NAME,
            ),
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
        max_length=IntegerRestrictions.ABOUT_TEXT,
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
        max_length=IntegerRestrictions.PROFILE_NAME,
    )
    sex = models.TextField(
        verbose_name='Пол',
        choices=GenderRoles,
    )
    age = models.PositiveSmallIntegerField(
        verbose_name='Возраст',
        validators=(
            MinValueValidator(
                IntegerRestrictions.AGE_MIN,
                message=Messages.AGE_MIN,
            ),
            MaxValueValidator(
                IntegerRestrictions.AGE_MAX,
                message=Messages.AGE_MAX,
            ),
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
            MinValueValidator(
                IntegerRestrictions.PRICE_MIN,
                message=Messages.PRICE_MIN,
            ),
        )
    )
    room_type = models.TextField(
        verbose_name='Тип коливинга',
        choices=ColivingTypes,
        default=ColivingTypes.DEFAULT,
    )

    class Meta(BaseProfileColiving.Meta):

        verbose_name = 'Коливинг'
        verbose_name_plural = 'Коливинги'
