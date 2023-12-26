import enum


class RoommateSearchStates(str, enum.Enum):
    """Класс, описывающий состояния ветви roommate_search бота."""
    (
        AGE,
        LOCATION,
        NEXT_PROFILE,
        NO_MATCHES,
        PROFILE,
        SEX,
        SEARCH_SETTINGS,
    ) = range(7)
