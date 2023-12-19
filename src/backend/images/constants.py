from django.db import models


class Restrictions(models.IntegerChoices):
    """
    Константы (числовые ограничения).
    """

    IMAGE_MAX_SIZE = 1 * 1024 * 1024


class Literals(models.TextChoices):
    """
    Константы (строковые литералы).
    """

    IMAGE_MAX_SIZE_MSG = f"Максимальный размер фото {int(
        Restrictions.IMAGE_MAX_SIZE / 1024 / 1024
    )} Мб."
