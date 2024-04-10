from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

import conversations.roommate_search.buttons as buttons
from conversations.roommate_search.buttons import AGE_BUTTONS

SEARCH_SETTINGS_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=buttons.OK_SETTINGS_BTN, callback_data=buttons.OK_SETTINGS_BTN
        ),
        InlineKeyboardButton(
            text=buttons.EDIT_SETTINGS_BTN,
            callback_data=buttons.EDIT_SETTINGS_BTN,
        ),
    )
)

SEX_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=buttons.MALE_BTN, callback_data=buttons.MALE_BTN),
        InlineKeyboardButton(text=buttons.FEMALE_BTN, callback_data=buttons.FEMALE_BTN),
    )
)

PROFILE_KEYBOARD = ReplyKeyboardMarkup.from_row(
    button_row=(
        KeyboardButton(text=buttons.LIKE_BTN),
        KeyboardButton(text=buttons.DISLIKE_BTN),
    ),
    resize_keyboard=True,
)

LIKE_PROFILE = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=buttons.YES_BTN, callback_data=buttons.SEE_PROFILE),
        InlineKeyboardButton(text=buttons.WAIT_BTN, callback_data=buttons.WAIT_BTN),
    )
)

NO_MATCHES_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=buttons.WAIT_BTN, callback_data=buttons.WAIT_BTN),
        InlineKeyboardButton(
            text=buttons.EDIT_SETTINGS_BTN,
            callback_data=buttons.EDIT_SETTINGS_BTN,
        ),
    )
)

NEXT_PROFILE = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=buttons.YES_BTN, callback_data=buttons.YES_BTN),
        InlineKeyboardButton(text=buttons.NO_BTN, callback_data=buttons.NO_BTN),
    )
)

AGE_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text=age, callback_data=age)
            for age in AGE_BUTTONS[i : i + 2]
        ]
        for i in range(0, len(AGE_BUTTONS), 2)
    ]
)
