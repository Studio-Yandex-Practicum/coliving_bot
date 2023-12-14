from django.db import models


class ColivingTypes(models.TextChoices):
    """
        Тип коливинга.
    """

    SEPARATE_ROOM = ('SR', 'Комната')
    SLEEPING_PLACE = ('SP', 'Спальное место')


class GenderRoles(models.TextChoices):
    """
        Гендерная принадлежность.
    """

    MAN = ('M', 'Мужчина')
    WOMAN = ('W', 'Женщина')


class Restrictions(models.IntegerChoices):
    """
        Числовые ограничения.
    """

    LOCATION_NAME_MIN = 2
    LOCATION_NAME_MAX = 50
    ABOUT_TEXT = 1000
    PROFILE_NAME = 30
    AGE_MIN = 18
    AGE_MAX = 99
    PRICE_MIN = 1
    PRICE_MAX = 100000
