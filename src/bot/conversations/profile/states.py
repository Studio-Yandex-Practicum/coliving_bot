import enum


class States(str, enum.Enum):
    """Класс, описывающий состояния бота."""

    (
        PROFILE,
        AGE,
        EDIT_AGE,
        SEX,
        EDIT_SEX,
        NAME,
        EDIT_NAME,
        LOCATION,
        EDIT_LOCATION,
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
