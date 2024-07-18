import enum


class States(int, enum.Enum):
    """Класс, описывающий состояния бота."""

    (
        AGE_MIN,
        AGE_MAX,
        LOCATION,
        NO_MATCHES,
        PROFILE,
        SEX,
        SEARCH_SETTINGS,
    ) = range(7)
