from django.db import models


class ColivingTypes(models.TextChoices):
    """
    Константы (тип коливинга).
    """

    ROOM = ("Комната", "Комната")
    PLACE = ("Спальное место", "Спальное место")


class Sex(models.TextChoices):
    """
    Константы (пол пользователя).
    """

    MAN = ("Парень", "Парень")
    WOMAN = ("Девушка", "Девушка")


class Restrictions(models.IntegerChoices):
    """
    Константы (числовые ограничения).
    """

    PROFILE_NAME_MIN = 2
    PROFILE_NAME_MAX = 30
    PROFILE_NAME_STR = 15
    AGE_MIN = 18
    AGE_MAX = 99
    PRICE_MIN = 0
    PRICE_MAX = 100000


class Literals(models.TextChoices):
    """
    Константы (строковые литералы).
    """

    NAME_CHECK = r"^[А-Яа-яA-Za-z\s'-]+$"
    NAME_CHECK_MESSAGE = "Числа и спец. символы не поддерживаются"
