from django.db import models

from profiles.models import Coliving, Profile

from .utils import images_directory_path
from .validators import image_size_validator


class BaseImage(models.Model):
    """
    Общие атрибуты объектов 'ColivingImage' и 'ProfileImage'.
    """

    image = models.ImageField(
        upload_to=images_directory_path, validators=(image_size_validator,)
    )
    file_id = models.TextField(
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        abstract = True
        default_related_name = "images"


class ColivingImage(BaseImage):
    """
    Конфигурация объекта 'ColivingImage'.
    """

    coliving = models.ForeignKey(Coliving, on_delete=models.CASCADE)

    class Meta(BaseImage.Meta):
        verbose_name = "Фото коливинга"
        verbose_name_plural = "Фото коливингов"

    def __str__(self):
        return f"colivings/{self.coliving_id}"


class ProfileImage(BaseImage):
    """
    Конфигурация объекта 'ProfileImage'.
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta(BaseImage.Meta):
        verbose_name = "Фото пользователя"
        verbose_name_plural = "Фото пользователей"

    def __str__(self):
        return f"profiles/{self.profile_id}"
