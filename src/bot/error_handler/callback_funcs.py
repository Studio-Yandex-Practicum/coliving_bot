import logging

from httpx import HTTPStatusError
from telegram import Update
from telegram.ext import ContextTypes

from error_handler.templates import ERROR_MESSAGE_TEMPLATE, LOGGING_MESSAGE_TEMPLATE

_LOGGER = logging.getLogger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Passes the error to the logger.
    Sends a telegram message to the user about the error.
    """
    error_text = LOGGING_MESSAGE_TEMPLATE.format(
        user_data=context.user_data, chat_data=context.chat_data
    )
    error_text = await _add_http_status_error_content(context, error_text)

    _LOGGER.error(error_text, exc_info=context.error)
    message = ERROR_MESSAGE_TEMPLATE.format(error=context.error)

    if isinstance(update, Update):
        await update.effective_chat.send_message(text=message)


async def _add_http_status_error_content(context, error_text):
    if isinstance(context.error, HTTPStatusError):
        response = context.error.response
        if 400 <= response.status_code < 500:
            content_str = response.content.decode("utf-8", "replace")
            error_text += f"Content: {content_str}"
    return error_text
