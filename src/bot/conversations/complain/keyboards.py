from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import conversations.complain.buttons as btns
from internal_requests.entities import Categories


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


NO_COMMENT_REPORT = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=btns.SKIP_BUTTON,
            callback_data=btns.SKIP_BUTTON,
        ),
    )
)


SCREENSHOT_OR_NOT_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=btns.SCREEN_YES_BUTTON,
            callback_data=btns.SCREEN_YES_BUTTON,
        ),
        InlineKeyboardButton(
            text=btns.SCREEN_NO_BUTTON,
            callback_data=btns.SCREEN_NO_BUTTON,
        ),
    )
)
CATEGORY_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=category, callback_data=category)]
        for category in Categories
    ]
)
