from django.db import models

from .constants import NAME_MAX_LEN, ABOUT_MAX_LEN


class UserFromTelegram(models.Model):
    """
        Объект 'Пользователь'.
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
        Объект 'Местоположение'.
    """

    name = models.CharField(
        verbose_name='Имя',
        max_length=NAME_MAX_LEN,
    )

    class Meta:

        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)


class AbstractProfileColiving(models.Model):
    """
        Общие атрибуты объектов 'Профиль' и 'Коливинг'.
    """

    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.CASCADE,
    )
    about = models.TextField(
        verbose_name='Описание',
        max_length=ABOUT_MAX_LEN,
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


class Profile(AbstractProfileColiving):
    """
        Объект 'Профиль'.
    """

    class Meta(AbstractProfileColiving.Meta):

        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Coliving(AbstractProfileColiving):
    """
        Объект 'Коливинг'.
    """

    host = models.ForeignKey(
        UserFromTelegram,
        related_name='colivings',
        on_delete=models.CASCADE,
    )

    class Meta(AbstractProfileColiving.Meta):

        verbose_name = 'Коливинг'
        verbose_name_plural = 'Коливинги'
