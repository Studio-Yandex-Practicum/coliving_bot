from django.db import models


class MatchStatuses(models.IntegerChoices):
    """
    Константы (статусы запросов).
    """

    is_pending = 0
    is_match = 1
    is_rejected = -1
