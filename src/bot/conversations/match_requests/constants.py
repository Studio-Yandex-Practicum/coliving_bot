from enum import Enum


class MatchStatus(Enum):
    """Cтатусы MatchRequest."""

    IS_PENDING = 0
    IS_MATCH = 1
    IS_REJECTED = -1


LIKE_ID_REGEX_GROUP = "like_id"
SENDER_ID_REGEX_GROUP = "sender"
