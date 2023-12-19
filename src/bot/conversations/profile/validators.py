from math import inf

from telegram import Update
from telegram.ext import ContextTypes


async def validate_integer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    value: str,
    min: float = -inf,
    max: float = inf,
    message: str = None,
) -> bool:
    if isinstance(value, int) or (
        value.isdigit() and not value.startswith('0')
    ):
        int_value = int(value)
        if min <= int_value <= max:
            return True

    await update.effective_message.reply_text(text=message)
    return False
