import logging

from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from error_handler.templates import ERROR_MESSAGE_TEMPLATE


async def error_handler(
        update: object, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Passes the error to the logger.
    Sends a telegram message to the user about the error.
    """
    logger = logging.getLogger("logger")
    logger.error("Exception while handling an update:", exc_info=context.error)
    message = ERROR_MESSAGE_TEMPLATE.format(error=context.error)
    user_chat_id = update["message"]["chat"]["id"]
    await context.bot.send_message(
        chat_id=user_chat_id, text=message, parse_mode=ParseMode.HTML
    )
