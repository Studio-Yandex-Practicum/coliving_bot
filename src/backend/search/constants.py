from django.db import models

ONE_MONTH = 30


class MatchStatuses(models.IntegerChoices):
    """
    Константы (статусы запросов).
    """

    is_pending = 0
    is_match = 1
    is_rejected = -1


class ReportCategories(models.TextChoices):
    """
    Константы (категории).
    """

    CATEGORY_1 = ("Категория 1", "Категория 1")
    CATEGORY_2 = ("Категория 2", "Категория 2")
    CATEGORY_3 = ("Категория 3", "Категория 3")
    OTHER = ("Другое", "Другое")


class ReportStatuses(models.TextChoices):
    """
    Константы (статусы жалоб).
    """

    RECEIVED = ("Получено", "Получено")
    VIEWED = ("Просмотрено", "Просмотрено")
    RESOLVED = ("Решено", "Решено")
    REJECTED = ("Отклонено", "Отклонено")
