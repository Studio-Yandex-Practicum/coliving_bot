from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

import conversations.match_requests.buttons as buttons

# from conversations.roommate_search.buttons import AGE_BUTTONS

# New
VIEW_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=buttons.SEE_PROFILE_BNT, callback_data=buttons.SEE_PROFILE_BNT
        ),
        InlineKeyboardButton(text=buttons.WAIT_BTN, callback_data=buttons.WAIT_BTN),
    )
)

PROFILE_KEYBOARD = ReplyKeyboardMarkup.from_row(
    button_row=(
        KeyboardButton(text=buttons.LIKE_BTN),
        KeyboardButton(text=buttons.DISLIKE_BTN),
    ),
    resize_keyboard=True,
)
