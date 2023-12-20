from math import inf
from typing import Union

from telegram import Update
from telegram.ext import ContextTypes

from conversations.profile.template import DEFAULT_ERROR_MESSAGE


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
