from django.db import models


class CityNames(models.TextChoices):
    """
        Возможные локации.
    """

    MSC = ('Москва', 'Москва')
    SPB = ('Санкт-Петербург', 'Санкт-Петербург')


class ColivingTypes(models.TextChoices):
    """
        Тип коливинга.
    """

    ROOM = ('Комната', 'Комната')
    PLACE = ('Спальное место', 'Спальное место')


class GenderRoles(models.TextChoices):
    """
        Гендерная принадлежность.
    """

    MAN = ('Мужчина', 'Мужчина')
    WOMAN = ('Женщина', 'Женщина')


class Restrictions(models.IntegerChoices):
    """
        Числовые ограничения.
    """

    ABOUT_TEST_MAX = 1000
    PROFILE_NAME_MIN = 3
    PROFILE_NAME_MAX = 30
    AGE_MIN = 18
    AGE_MAX = 99
    PRICE_MIN = 1
    PRICE_MAX = 100000


class Literals(models.TextChoices):
    """
        Строковые литералы.
    """

    NAME_CHECK = r'^[А-Яа-яA-Za-z\s]+$'
    NAME_CHECK_MESSAGE = 'Числа и спец. символы не поддерживаются'
