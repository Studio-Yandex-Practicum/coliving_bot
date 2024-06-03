import enum


class States(int, enum.Enum):
    """Класс, описывающий состояния бота."""

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
        ROOMMATE,
        NEXT_ROOMMATE,
        NO_ROOMMATES,
        EDIT_ROOM_TYPE,
        EDIT_ABOUT_ROOM,
        EDIT_PRICE,
        EDIT_PHOTO_ROOM,
        EDIT_CONFIRMATION,
        EDIT_LOCATION,
        DELETE_COLIVING,
        TRANSFER_COLIVING,
        COLIVING_ROOMMATE,
        COLIVING_CURRENT_USER,
    ) = range(22)
