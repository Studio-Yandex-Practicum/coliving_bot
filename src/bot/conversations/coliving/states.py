import enum


class ColivingStates(str, enum.Enum):
    """Класс, описывающий состояния ветви coliving бота."""

    (HELLO, COLIVING, LOCATION, ROOM_TYPE, ABOUT_ROOM, PRICE, PHOTO_ROOM,
     CONFIRMATION, EDIT, IS_VISIBLE, ROOMMATES, EDIT_ROOM_TYPE, EDIT_ABOUT_ROOM, EDIT_PRICE,
     EDIT_PHOTO, EDIT_CONFIRMATION) = range(16)