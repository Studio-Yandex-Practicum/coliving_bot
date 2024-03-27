from telegram import Update
from telegram.ext import ContextTypes

from .templates import BUTTON_ERROR_MSG


async def handle_text_input_instead_of_choosing_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await update.effective_message.reply_text(
        text=BUTTON_ERROR_MSG,
    )
