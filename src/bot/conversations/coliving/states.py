import enum


class ColivingStates(str, enum.Enum):
    """Класс, описывающий состояния ветви coliving бота."""

    (HELLO, COLIVING, LOCATION, ROOM_TYPE, ABOUT_ROOM, PRICE, PHOTO_ROOM,
     CONFIRMATION, ROOMMATES, EDIT, EDIT_ABOUT_ROOM, EDIT_PRICE,
     EDIT_PHOTO) = range(13)
