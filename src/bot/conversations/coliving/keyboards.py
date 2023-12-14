from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
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

# LOCATION_MOSCOW_KEYBOARD = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(
#                 text='Москва',
#                 callback_data='moscow_city'
#             ),
#         ]
#     ]
# )

# LOCATION_SPB_KEYBOARD = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(
#                 text='Санкт-Петербург',
#                 callback_data='spb_city'
#             ),
#         ]
#     ]
# )

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

CONFIRMATION_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Да, верно',
                callback_data='confirm'
            ),
        ]
    ]
)

EDIT_PROFILE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Изменить коливинг профиль',
                callback_data='edit_profile'
            ),
        ]
    ]
)

# Заполнить заново
# Описание
# Цена
# Фотография

WHAT_EDIT_PROFILE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Заполнить заново',
                callback_data='fill_again'
            ),
            InlineKeyboardButton(
                text='Описание',
                callback_data='description'
            ),
            InlineKeyboardButton(
                text='Цена',
                callback_data='price'
            ),
            InlineKeyboardButton(
                text='Фотография',
                callback_data='send_photo'
            ),
        ]
    ]
)

# Да, верно
# Отменить редактирование
# Продолжить редактирование

CONFIRMATION_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Да, подтвердить',
                callback_data='confirm'
            ),
        ]
    ]
)

CANCEL_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отменить редактирование',
                callback_data='cancel'
            ),
        ]
    ]
)

CONTINUE_EDIT_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Продолжить редактирование',
                callback_data='continue_editing'
            ),
        ]
    ]
)

# Изменить коливинг профиль
# Скрыть из поиска |  Показать в поиске
# Посмотреть анкеты соседей
# Просмотры
# Передача коливинга
# Вернуться

COLIVING_PROFILE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Изменить коливинг профиль',
                callback_data='edit_profile'
            ),
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
        ]
    ]
)

# Скрыть из поиска |  Показать в поиске

SHOW_SEARCH_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [

            InlineKeyboardButton(
                text='Показать в поиске',
                callback_data='show'
            ),
        ]
    ]
)

HIDE_SEARCH_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [

            InlineKeyboardButton(
                text='Скрыть из поиска',
                callback_data='hide'
            ),
        ]
    ]
)

# Выбор

CHOOSE_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [

            InlineKeyboardButton(
                text='Скрыть из поиска',
                callback_data='confirm'
            ),
        ]
    ]
)

# Пригласить в коливинг | Удалить из коливинга
# Пожаловаться на пользователя

INVITE_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [

            InlineKeyboardButton(
                text='Пригласить в коливинг',
                callback_data='invite_roommate'
            ),
        ]
    ]
)

DELETE_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [

            InlineKeyboardButton(
                text='Удалить из коливинга',
                callback_data='delete_roommate'
            ),
        ]
    ]
)

REPORT_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [

            InlineKeyboardButton(
                text='Пожаловаться на пользователя',
                callback_data='report_to'
            ),
        ]
    ]
)

CONFIRMATION_PROFILE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Да, удалить',
                callback_data='confirm'
            ),
        ]
    ]
)
