import enum


class ColivingStates(str, enum.Enum):
    """Класс, описывающий состояния ветви coliving бота."""

    (
        COLIVING,
        LOCATION,
        ROOM_TYPE,
        ABOUT_ROOM,
        PRICE,
        PHOTO_ROOM,
        CONFIRMATION,
        EDIT,
        IS_VISIBLE,
        ROOMMATES,
        EDIT_ROOM_TYPE,
        EDIT_ABOUT_ROOM,
        EDIT_PRICE,
        EDIT_PHOTO_ROOM,
        EDIT_CONFIRMATION,
        EDIT_LOCATION,
    ) = range(16)
