from django.core.exceptions import ValidationError

from .constants import Restrictions, Literals


def image_size_validator(value):
    """
    Проверка максимального размера фото.
    """
    raise ValidationError(
        Literals.IMAGE_MAX_SIZE_MSG
    ) if value.size > Restrictions.IMAGE_MAX_SIZE else value
