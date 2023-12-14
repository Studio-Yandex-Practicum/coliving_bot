import uuid

from django.db import models

from profiles.models import Profile, Coliving


class BaseImage(models.Model):
    """
        Общие атрибуты объектов 'ColivingImage' и 'ProfileImage'.
    """

    image = models.ImageField(upload_to='images/')
    file_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True,
    )

    class Meta:

        abstract = True
        default_related_name = 'images'


class ColivingImage(BaseImage):
    """
        Объект 'ColivingImage'.
    """

    coliving = models.ForeignKey(Coliving, on_delete=models.CASCADE)

    class Meta(BaseImage.Meta):

        verbose_name = 'Изображение коливинга'
        verbose_name_plural = 'Изображения коливингов'


class ProfileImage(BaseImage):
    """
        Объект 'ProfileImage'.
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta(BaseImage.Meta):

        verbose_name = 'Изображение пользователя'
        verbose_name_plural = 'Изображения пользователей'
