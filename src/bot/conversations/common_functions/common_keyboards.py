from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .common_buttons import CANCEL_BUTTON, HIDE_SEARCH_BUTTON, SHOW_SEARCH_BUTTON

CANCEL_KEYBOARD = InlineKeyboardMarkup.from_row(
    button_row=(InlineKeyboardButton(text=CANCEL_BUTTON, callback_data=CANCEL_BUTTON),)
)

SEARCH_BUTTON = InlineKeyboardButton(
    text=HIDE_SEARCH_BUTTON, callback_data="is_visible:False"
)
HIDE_BUTTON = InlineKeyboardButton(
    text=SHOW_SEARCH_BUTTON, callback_data="is_visible:True"
)
