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

    CATEGORY_SPAM = ("Спам", "Спам")
    CATEGORY_INCORRECT_DATA = (
        "Не совпадают личные данные",
        "Не совпадают личные данные",
    )
    CATEGORY_CHEATER = ("Мошенник", "Мошенник")
    CATEGORY_PROHIB_ACTIV = ("Запрещенная деятельность", "Запрещенная деятельность")
    CATEGORY_BAD_LANG = ("Оскорбления, мат", "Оскорбления, мат")
    CATEGORY_OTHER = ("Другое", "Другое")


class ReportStatuses(models.TextChoices):
    """
    Константы (статусы жалоб).
    """

    RECEIVED = ("Получено", "Получено")
    VIEWED = ("Просмотрено", "Просмотрено")
    RESOLVED = ("Решено", "Решено")
    REJECTED = ("Отклонено", "Отклонено")


ALREADY_REPORTED_TEXT = "Пара reported_user - reporter уже есть в БД."
ACCEPT_REPORT_TEXT = "Жалоба была принята. {username} заблокирован!"
REJECT_REPORT_TEXT = "Жалоба была отклонена!"
