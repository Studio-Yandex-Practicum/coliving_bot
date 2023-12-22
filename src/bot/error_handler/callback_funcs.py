import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from error_handler.templates import (
    ERROR_MESSAGE_TEMPLATE,
    LOGGING_MESSAGE_TEMPLATE
)


async def error_handler(
        update: object, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Passes the error to the logger.
    Sends a telegram message to the user about the error.
    """
    logger = logging.getLogger("logger")
    error_text = LOGGING_MESSAGE_TEMPLATE.format(
        user_data=context.user_data, chat_data=context.chat_data
    )
    logger.error(error_text, exc_info=context.error)
    message = ERROR_MESSAGE_TEMPLATE.format(error=context.error)

    if isinstance(update, Update):
        await update.effective_chat.send_message(
            text=message, parse_mode=ParseMode.HTML
        )
