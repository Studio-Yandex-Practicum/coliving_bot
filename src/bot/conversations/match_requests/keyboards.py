from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from conversations.match_requests import buttons as buttons

PROFILE_KEYBOARD = ReplyKeyboardMarkup.from_row(
    button_row=(
        KeyboardButton(text=buttons.LIKE_BTN),
        KeyboardButton(text=buttons.DISLIKE_BTN),
    ),
    resize_keyboard=True,
)


async def get_like_or_dislike_keyboard(like_id: int, telegram_id: int):
    like_or_dislike_keyboard = InlineKeyboardMarkup.from_row(
        button_row=(
            InlineKeyboardButton(
                text=buttons.LIKE_BTN,
                callback_data=rf"{like_id}:{telegram_id}:{buttons.LIKE_BTN}",
            ),
            InlineKeyboardButton(
                text=buttons.DISLIKE_BTN,
                callback_data=rf"{like_id}:{telegram_id}:{buttons.DISLIKE_BTN}",
            ),
        ),
    )
    return like_or_dislike_keyboard
