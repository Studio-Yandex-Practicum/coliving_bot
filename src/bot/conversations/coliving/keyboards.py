from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


HELLO_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Начать',
                callback_data='hello',
            )
        ],
    ],
)

CONFIRMATION_KEYBOARD = InlineKeyboardButton(
    text='Да, подтвердить',
    callback_data='confirm'
)

CANCEL_KEYBOARD = InlineKeyboardButton(
    text='Отменить',
    callback_data='cancel'
)

# Москва
# Санкт-Петербург

LOCATION_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        [
            InlineKeyboardButton(
                text='Москва',
                callback_data='moscow_city'
            ),
            InlineKeyboardButton(
                text='Санкт-Петербург',
                callback_data='spb_city'
            ),
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
                text='Спальное место в комнате',
                callback_data='bed_in_room'
            ),
            InlineKeyboardButton(
                text='Комната в квартире',
                callback_data='room_in_apartment'
            ),
            InlineKeyboardButton(
                text='Комната в доме',
                callback_data='room_in_house'
            ),
        ]
    )
)

# Да, верно
# Изменить коливинг профиль

EDIT_PROFILE_KEYBOARD = InlineKeyboardButton(
        text='Изменить коливинг профиль',
        callback_data='edit_profile'
)

CONFIRM_OR_EDIT_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        CONFIRMATION_KEYBOARD,
        EDIT_PROFILE_KEYBOARD,
    )
)

# Заполнить заново
# Описание
# Цена
# Фотография

WHAT_EDIT_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        [
            InlineKeyboardButton(
                text='Заполнить заново',
                callback_data='edit_fill_again'
            ),
            InlineKeyboardButton(
                text='Тип помещения',
                callback_data='edit_room_type'
            ),
            InlineKeyboardButton(
                text='Описание',
                callback_data='edit_description'
            ),
            InlineKeyboardButton(
                text='Цена',
                callback_data='edit_price'
            ),
            InlineKeyboardButton(
                text='Фото квартиры',
                callback_data='edit_send_photo'
            ),
        ]
    )
)

# Скрыть из поиска |  Показать в поиске

SHOW_SEARCH_KEYBOARD = InlineKeyboardButton(
    text='Показать в поиске',
    callback_data='show',
)

HIDE_SEARCH_KEYBOARD = InlineKeyboardButton(
    text='Скрыть из поиска',
    callback_data='hide',
)

IS_VISIBLE_OR_NOT_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        SHOW_SEARCH_KEYBOARD,
        HIDE_SEARCH_KEYBOARD,
    )
)

# Да, верно
# Отменить редактирование
# Продолжить редактирование

EDIT_CONFIRMATION_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        CONFIRMATION_KEYBOARD,
        InlineKeyboardButton(
            text='Отменить редактирование',
            callback_data='cancel'
        ),
        InlineKeyboardButton(
            text='Продолжить редактирование',
            callback_data='continue_editing'
        ),
    )
)

# + Скрыть из поиска |  Показать в поиске

COLIVING_PROFILE_KEYBOARD_VISIBLE = InlineKeyboardMarkup.from_column(
    button_column=(
        EDIT_PROFILE_KEYBOARD,
        HIDE_SEARCH_KEYBOARD,
        InlineKeyboardButton(
            text='Посмотреть анкеты соседей',
            callback_data='roommates_profiles'
        ),
        InlineKeyboardButton(
            text='Просмотры',
            callback_data='views'
        ),
        InlineKeyboardButton(
            text='Передача коливинга',
            callback_data='transfer_to'
        ),
        InlineKeyboardButton(
            text='Вернуться в меню',
            callback_data='go_to_menu'
        ),
    )
)

# + Показать в поиске

COLIVING_PROFILE_KEYBOARD_NOT_VISIBLE = InlineKeyboardMarkup.from_column(
    button_column=(
        EDIT_PROFILE_KEYBOARD,
        SHOW_SEARCH_KEYBOARD,
        InlineKeyboardButton(
            text='Посмотреть анкеты соседей',
            callback_data='roommates_profiles'
        ),
        InlineKeyboardButton(
            text='Просмотры',
            callback_data='views'
        ),
        InlineKeyboardButton(
            text='Передача коливинга',
            callback_data='transfer_to'
        ),
        InlineKeyboardButton(
            text='Вернуться в меню',
            callback_data='go_to_menu'
        ),
    )
)

# Выбор

# CHOOSE_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [

#             InlineKeyboardButton(
#                 text='Выбран',
#                 callback_data='confirm'
#             ),
#         ]
#     ]
# )

# Пригласить в коливинг | Удалить из коливинга
# Пожаловаться на пользователя

INVITE_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardButton(
    text='Пригласить в коливинг',
    callback_data='invite_roommate'
)

DELETE_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardButton(
    text='Удалить из коливинга',
    callback_data='delete_roommate'
)

REPORT_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardButton(
    text='Пожаловаться на пользователя',
    callback_data='report_to'
)

CONFIRMATION_DELETE_KEYBOARD = InlineKeyboardButton(
    text='Да, удалить',
    callback_data='confirm'
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
