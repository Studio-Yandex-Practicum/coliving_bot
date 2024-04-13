from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

import conversations.coliving_search.buttons as buttons

SEARCH_SETTINGS_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=buttons.OK_SETTINGS_BTN, callback_data=buttons.OK_SETTINGS_BTN
        ),
        InlineKeyboardButton(
            text=buttons.EDIT_SETTINGS_BTN,
            callback_data=buttons.EDIT_SETTINGS_BTN,
        ),
        InlineKeyboardButton(
            text=buttons.TO_MENU_BTN, callback_data=buttons.TO_MENU_BTN
        ),
    )
)

ROOM_TYPE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=buttons.TYPE_ROOM_BTN, callback_data=buttons.TYPE_ROOM_BTN
        ),
        InlineKeyboardButton(
            text=buttons.TYPE_BED_BTN, callback_data=buttons.TYPE_BED_BTN
        ),
    )
)

COLIVING_KEYBOARD = ReplyKeyboardMarkup.from_row(
    button_row=(
        KeyboardButton(text=buttons.LIKE_BTN),
        KeyboardButton(text=buttons.DISLIKE_BTN),
        KeyboardButton(text=buttons.TO_MENU_BTN),
    ),
    resize_keyboard=True,
)

NO_MATCHES_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=buttons.TO_MENU_BTN, callback_data=buttons.TO_MENU_BTN
        ),
        InlineKeyboardButton(
            text=buttons.EDIT_SETTINGS_BTN,
            callback_data=buttons.EDIT_SETTINGS_BTN,
        ),
    )
)

NEXT_COLIVING = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=buttons.YES_BTN, callback_data=buttons.YES_BTN),
        InlineKeyboardButton(
            text=buttons.TO_MENU_BTN, callback_data=buttons.TO_MENU_BTN
        ),
    )
)
