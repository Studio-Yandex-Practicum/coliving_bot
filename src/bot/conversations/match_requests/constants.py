from enum import Enum


class MatchStatus(Enum):
    """Cтатусы MatchRequest."""

    IS_PENDING = 0
    IS_MATCH = 1
    IS_REJECTED = -1


TG_ID_REGEX_GRP = "tg_id"
