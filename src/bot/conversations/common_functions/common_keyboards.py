from telegram import InlineKeyboardButton

from .common_buttons import HIDE_SEARCH_BUTTON, SHOW_SEARCH_BUTTON

SEARCH_BUTTON = InlineKeyboardButton(
    text=SHOW_SEARCH_BUTTON,
    callback_data=SHOW_SEARCH_BUTTON,
)
HIDE_BUTTON = InlineKeyboardButton(
    text=HIDE_SEARCH_BUTTON,
    callback_data=HIDE_SEARCH_BUTTON,
)
