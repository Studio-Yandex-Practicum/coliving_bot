from django.core.exceptions import ValidationError

from .constants import Literals, Restrictions


def image_size_validator(value):
    """
    Проверка максимального размера фото.
    """
    if value.size > Restrictions.IMAGE_MAX_SIZE:
        raise ValidationError(Literals.IMAGE_MAX_SIZE_MSG)

    return value
