import enum


class States(int, enum.Enum):
    """Класс, описывающий состояния бота."""

    (
        PROFILE,
        AGE,
        SEX,
        NAME,
        LOCATION,
        ABOUT_YOURSELF,
        EDIT_ABOUT_YOURSELF,
        EDIT,
        PHOTO,
        EDIT_PHOTO,
        CONFIRMATION,
        EDIT_CONFIRMATION,
        VISIBLE,
        MENU,
    ) = range(14)
