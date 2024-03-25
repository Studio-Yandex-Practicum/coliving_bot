import enum


class States(int, enum.Enum):
    """Класс, описывающий состояния бота."""

    (
        AGE,
        LOCATION,
        NEXT_PROFILE,
        NO_MATCHES,
        PROFILE,
        SEX,
        SEARCH_SETTINGS,
    ) = range(7)
