import enum


class States(int, enum.Enum):
    """Класс, описывающий состояния бота."""

    (
        INVITATION_START,
        INVITATION_YES,
        INVITATION_NO,
    ) = range(3)
