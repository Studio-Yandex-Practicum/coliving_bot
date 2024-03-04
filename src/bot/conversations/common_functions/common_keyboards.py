from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .common_buttons import CANCEL_BUTTON


CANCEL_KEYBOARD = InlineKeyboardMarkup.from_row(
    button_row=(InlineKeyboardButton(text=CANCEL_BUTTON, callback_data=CANCEL_BUTTON),)
)