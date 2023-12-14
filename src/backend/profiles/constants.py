from django.db import models


class ColivingTypes(models.TextChoices):
    """
        Типы коливинга.
    """

    DEFAULT = 'Комната'
    SLEEPING_PLACE = 'Спальное место'


class IntegerRestrictions(models.IntegerChoices):
    """
        Числовые ограничения.
    """

    LOCATION_NAME = 100
    ABOUT_TEXT = 1000
    PROFILE_NAME = 30
    AGE_MIN = 18
    AGE_MAX = 99
    PRICE_MIN = 1


class GenderRoles(models.TextChoices):
    """
        Гендерная принадлежность.
    """

    MALE = 'Мужчина'
    FEMALE = 'Женщина'


class Messages(models.TextChoices):
    """
        Сообщения.
    """

    AGE_MIN = 'Регистрация возможна с 18 лет'
    AGE_MAX = 'Число не поддерживается'
    PRICE_MIN = 'Укажите значение больше 0'
    LOCATION_NAME = 'Имя локации больше 100 символов не поддерживается'
