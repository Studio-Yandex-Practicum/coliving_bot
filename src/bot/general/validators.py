from math import inf
from typing import Union

from conversations.profile.templates import (
    BUTTON_ERROR_MSG,
    DEFAULT_ERROR_MESSAGE,
    PHOTO_ERROR_MESSAGE,
)
from telegram import Update
from telegram.ext import ContextTypes


async def value_is_in_range_validator(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    value: Union[int, str],
    min: float = -inf,
    max: float = inf,
    message: str = DEFAULT_ERROR_MESSAGE,
) -> bool:
    if isinstance(value, int) or value.isdigit():
        int_value = int(value)
        if min <= int_value <= max:
            return True

    await update.effective_message.reply_text(text=message)

    return False


async def handle_text_input_instead_of_choosing_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await update.effective_message.reply_text(
        BUTTON_ERROR_MSG,
    )


async def handle_text_input_instead_of_send_photo(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await update.effective_message.reply_text(
        PHOTO_ERROR_MESSAGE,
    )
