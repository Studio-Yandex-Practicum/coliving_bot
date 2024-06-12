from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

import conversations.complain.buttons as btns

SCREENSHOT_KEYBOARD = ReplyKeyboardMarkup.from_button(
    KeyboardButton(text=btns.SAVE_SCREENSHOT_BUTTON), resize_keyboard=True
)


async def get_report_or_not_keyboard(reported_user_id: int):
    report_or_not_keyboard = InlineKeyboardMarkup.from_column(
        button_column=(
            InlineKeyboardButton(
                text=btns.REPORT_YES_BUTTON,
                callback_data=rf"{reported_user_id}:{btns.REPORT_YES_BUTTON}",
            ),
            InlineKeyboardButton(
                text=btns.REPORT_NO_BUTTON,
                callback_data=rf"{reported_user_id}:{btns.REPORT_NO_BUTTON}",
            ),
        ),
    )
    return report_or_not_keyboard


async def get_screenshot_or_not_keyboard():
    screenshot_or_not_keyboard = InlineKeyboardMarkup.from_column(
        button_column=(
            InlineKeyboardButton(
                text=btns.SCREEN_YES_BUTTON,
                callback_data=btns.SCREEN_YES_BUTTON,
            ),
            InlineKeyboardButton(
                text=btns.SCREEN_NO_BUTTON,
                callback_data=btns.SCREEN_NO_BUTTON,
            ),
        ),
    )
    return screenshot_or_not_keyboard


async def get_category_keyboard():
    category_keyboard = InlineKeyboardMarkup.from_column(
        button_column=(
            InlineKeyboardButton(
                text=btns.CATEGORY_SPAM_BUTTON,
                callback_data=btns.CATEGORY_SPAM_BUTTON,
            ),
            InlineKeyboardButton(
                text=btns.CATEGORY_INCORRECT_DATA_BUTTON,
                callback_data=btns.CATEGORY_INCORRECT_DATA_BUTTON,
            ),
            InlineKeyboardButton(
                text=btns.CATEGORY_CHEATER_BUTTON,
                callback_data=btns.CATEGORY_CHEATER_BUTTON,
            ),
            InlineKeyboardButton(
                text=btns.CATEGORY_BAD_LANG_BUTTON,
                callback_data=btns.CATEGORY_BAD_LANG_BUTTON,
            ),
            InlineKeyboardButton(
                text=btns.CATEGORY_PROHIB_ACTIV_BUTTON,
                callback_data=btns.CATEGORY_PROHIB_ACTIV_BUTTON,
            ),
            InlineKeyboardButton(
                text=btns.CATEGORY_OTHER_BUTTON,
                callback_data=btns.CATEGORY_OTHER_BUTTON,
            ),
        ),
    )
    return category_keyboard
