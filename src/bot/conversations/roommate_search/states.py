import enum


class States(int, enum.Enum):
    """Класс, описывающий состояния бота."""

    (
        AGE_MIN,
        AGE_MAX,
        LOCATION,
        NEXT_PROFILE,
        NO_MATCHES,
        PROFILE,
        SEX,
        SEARCH_SETTINGS,
    ) = range(8)
