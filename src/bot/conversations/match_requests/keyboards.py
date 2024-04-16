from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

import conversations.match_requests.buttons as buttons

# from conversations.roommate_search.buttons import AGE_BUTTONS


PROFILE_KEYBOARD = ReplyKeyboardMarkup.from_row(
    button_row=(
        KeyboardButton(text=buttons.LIKE_BTN),
        KeyboardButton(text=buttons.DISLIKE_BTN),
    ),
    resize_keyboard=True,
)


async def get_view_profile_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    view_profile_keyboard = InlineKeyboardMarkup.from_column(
        button_column=(
            InlineKeyboardButton(
                text=buttons.SEE_PROFILE_BNT,
                callback_data=f"{telegram_id}:{buttons.SEE_PROFILE_BNT}",
            ),
            InlineKeyboardButton(text=buttons.WAIT_BTN, callback_data=buttons.WAIT_BTN),
        )
    )
    return view_profile_keyboard


async def get_like_or_dislike_keyboard(telegram_id: int):
    like_or_dislike_keyboard = InlineKeyboardMarkup.from_row(
        button_row=(
            InlineKeyboardButton(
                text=buttons.LIKE_BTN,
                callback_data=rf"{telegram_id}:{buttons.LIKE_BTN}",
            ),
            InlineKeyboardButton(
                text=buttons.DISLIKE_BTN,
                callback_data=rf"{telegram_id}:{buttons.DISLIKE_BTN}",
            ),
        ),
    )
    return like_or_dislike_keyboard
