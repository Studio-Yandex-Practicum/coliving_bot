from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from conversations.coliving.templates import (
    BTN_BED_IN_ROOM,
    BTN_CANCEL,
    BTN_CANCEL_EDIT,
    BTN_CONFIRM,
    BTN_DELETE_CONFIRM,
    BTN_DELETE_ROOMMATES,
    BTN_EDIT_ABOUT_ROOM,
    BTN_EDIT_CONTINUE,
    BTN_EDIT_PHOTO,
    BTN_EDIT_PRICE,
    BTN_EDIT_PROFILE,
    BTN_EDIT_ROOM_TYPE,
    BTN_FILL_AGAIN,
    BTN_GO_TO_MENU,
    BTN_HIDE,
    BTN_INVITE_ROOMMATES,
    BTN_LABEL_BED_IN_ROOM,
    BTN_LABEL_CANCEL,
    BTN_LABEL_CANCEL_EDIT,
    BTN_LABEL_CONFIRM,
    BTN_LABEL_DELETE_CONFIRM,
    BTN_LABEL_DELETE_ROOMMATES,
    BTN_LABEL_EDIT_ABOUT_ROOM,
    BTN_LABEL_EDIT_CONTINUE,
    BTN_LABEL_EDIT_PHOTO,
    BTN_LABEL_EDIT_PRICE,
    BTN_LABEL_EDIT_PROFILE_KEYBOARD,
    BTN_LABEL_EDIT_ROOM_TYPE,
    BTN_LABEL_FILL_AGAIN,
    BTN_LABEL_GO_TO_MENU,
    BTN_LABEL_HIDE_SEARCH_KEYBOARD,
    BTN_LABEL_INVITE_ROOMMATES,
    BTN_LABEL_MOSCOW,
    BTN_LABEL_REPORT_ROOMMATES,
    BTN_LABEL_ROOM_IN_APPARTMENT,
    BTN_LABEL_ROOM_IN_HOUSE,
    BTN_LABEL_ROOMMATES,
    BTN_LABEL_SHOW,
    BTN_LABEL_SPB,
    BTN_LABEL_TRANSFER_TO,
    BTN_LABEL_VIEWS,
    BTN_MOSCOW,
    BTN_REPORT_ROOMMATES,
    BTN_ROOM_IN_APPARTMENT,
    BTN_ROOM_IN_HOUSE,
    BTN_ROOMMATES,
    BTN_SHOW,
    BTN_SPB,
    BTN_TRANSFER_TO,
    BTN_VIEWS,
)

CONFIRMATION_KEYBOARD = InlineKeyboardButton(
    text=BTN_LABEL_CONFIRM, callback_data=BTN_CONFIRM
)

CANCEL_KEYBOARD = InlineKeyboardButton(
    text=BTN_LABEL_CANCEL, callback_data=BTN_CANCEL
)

# Москва
# Санкт-Петербург

LOCATION_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        [
            InlineKeyboardButton(
                text=BTN_LABEL_MOSCOW, callback_data=BTN_MOSCOW
            ),
            InlineKeyboardButton(text=BTN_LABEL_SPB, callback_data=BTN_SPB),
        ]
    )
)

# Спальное место в комнате
# Комната в квартире
# Комната в доме

ROOM_TYPE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        [
            InlineKeyboardButton(
                text=BTN_LABEL_BED_IN_ROOM, callback_data=BTN_BED_IN_ROOM
            ),
            InlineKeyboardButton(
                text=BTN_LABEL_ROOM_IN_APPARTMENT,
                callback_data=BTN_ROOM_IN_APPARTMENT,
            ),
            InlineKeyboardButton(
                text=BTN_LABEL_ROOM_IN_HOUSE, callback_data=BTN_ROOM_IN_HOUSE
            ),
        ]
    )
)

# Да, верно
# Изменить коливинг профиль

EDIT_PROFILE_KEYBOARD = InlineKeyboardButton(
    text=BTN_LABEL_EDIT_PROFILE_KEYBOARD, callback_data=BTN_EDIT_PROFILE
)

CONFIRM_OR_EDIT_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        CONFIRMATION_KEYBOARD,
        EDIT_PROFILE_KEYBOARD,
    )
)

WHAT_EDIT_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        [
            InlineKeyboardButton(
                text=BTN_LABEL_FILL_AGAIN, callback_data=BTN_FILL_AGAIN
            ),
            InlineKeyboardButton(
                text=BTN_LABEL_EDIT_ROOM_TYPE, callback_data=BTN_EDIT_ROOM_TYPE
            ),
            InlineKeyboardButton(
                text=BTN_LABEL_EDIT_ABOUT_ROOM,
                callback_data=BTN_EDIT_ABOUT_ROOM,
            ),
            InlineKeyboardButton(
                text=BTN_LABEL_EDIT_PRICE, callback_data=BTN_EDIT_PRICE
            ),
            InlineKeyboardButton(
                text=BTN_LABEL_EDIT_PHOTO, callback_data=BTN_EDIT_PHOTO
            ),
        ]
    )
)

# Скрыть из поиска |  Показать в поиске

SHOW_SEARCH_KEYBOARD = InlineKeyboardButton(
    text=BTN_LABEL_SHOW,
    callback_data=BTN_SHOW,
)

HIDE_SEARCH_KEYBOARD = InlineKeyboardButton(
    text=BTN_LABEL_HIDE_SEARCH_KEYBOARD,
    callback_data=BTN_HIDE,
)

IS_VISIBLE_OR_NOT_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        SHOW_SEARCH_KEYBOARD,
        HIDE_SEARCH_KEYBOARD,
    )
)

EDIT_CONFIRMATION_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        CONFIRMATION_KEYBOARD,
        InlineKeyboardButton(
            text=BTN_LABEL_CANCEL_EDIT, callback_data=BTN_CANCEL_EDIT
        ),
        InlineKeyboardButton(
            text=BTN_LABEL_EDIT_CONTINUE, callback_data=BTN_EDIT_CONTINUE
        ),
    )
)

# + Скрыть из поиска |  Показать в поиске

COLIVING_PROFILE_KEYBOARD_VISIBLE = InlineKeyboardMarkup.from_column(
    button_column=(
        EDIT_PROFILE_KEYBOARD,
        HIDE_SEARCH_KEYBOARD,
        InlineKeyboardButton(
            text=BTN_LABEL_ROOMMATES, callback_data=BTN_ROOMMATES
        ),
        InlineKeyboardButton(text=BTN_LABEL_VIEWS, callback_data=BTN_VIEWS),
        InlineKeyboardButton(
            text=BTN_LABEL_TRANSFER_TO, callback_data=BTN_TRANSFER_TO
        ),
        InlineKeyboardButton(
            text=BTN_LABEL_GO_TO_MENU, callback_data=BTN_GO_TO_MENU
        ),
    )
)

# + Показать в поиске

COLIVING_PROFILE_KEYBOARD_NOT_VISIBLE = InlineKeyboardMarkup.from_column(
    button_column=(
        EDIT_PROFILE_KEYBOARD,
        SHOW_SEARCH_KEYBOARD,
        InlineKeyboardButton(
            text=BTN_LABEL_ROOMMATES, callback_data=BTN_ROOMMATES
        ),
        InlineKeyboardButton(text=BTN_LABEL_VIEWS, callback_data=BTN_VIEWS),
        InlineKeyboardButton(
            text=BTN_LABEL_TRANSFER_TO, callback_data=BTN_TRANSFER_TO
        ),
        InlineKeyboardButton(
            text=BTN_LABEL_GO_TO_MENU, callback_data=BTN_GO_TO_MENU
        ),
    )
)

# Выбор

# CHOOSE_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [

#             InlineKeyboardButton(
#                 text='Выбран',
#                 callback_data=BTN_CONFIRM
#             ),
#         ]
#     ]
# )

# Пригласить в коливинг | Удалить из коливинга
# Пожаловаться на пользователя

INVITE_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardButton(
    text=BTN_LABEL_INVITE_ROOMMATES, callback_data=BTN_INVITE_ROOMMATES
)

DELETE_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardButton(
    text=BTN_LABEL_DELETE_ROOMMATES, callback_data=BTN_DELETE_ROOMMATES
)

REPORT_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardButton(
    text=BTN_LABEL_REPORT_ROOMMATES, callback_data=BTN_REPORT_ROOMMATES
)

CONFIRMATION_DELETE_KEYBOARD = InlineKeyboardButton(
    text=BTN_LABEL_DELETE_CONFIRM, callback_data=BTN_DELETE_CONFIRM
)

ROOMMATES_INVITE_REPORT_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        INVITE_ROOMMATES_PROFILE_KEYBOARD,
        REPORT_ROOMMATES_PROFILE_KEYBOARD,
    )
)

ROOMMATES_INVITE_REPORT_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        DELETE_ROOMMATES_PROFILE_KEYBOARD,
        REPORT_ROOMMATES_PROFILE_KEYBOARD,
    )
)


CONFIRM_ROOMMATES_INVITE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        CONFIRMATION_KEYBOARD,
        CANCEL_KEYBOARD,
    )
)

REPORT_OR_CANCEL_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        REPORT_ROOMMATES_PROFILE_KEYBOARD,
        CANCEL_KEYBOARD,
    )
)
