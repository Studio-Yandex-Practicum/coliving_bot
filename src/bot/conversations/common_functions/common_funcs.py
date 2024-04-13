from functools import wraps

from httpx import HTTPStatusError, codes
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.common_functions.common_templates as templates
from internal_requests import api_service


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяет текущий диалог."""
    await update.effective_message.reply_text(
        text=templates.CANCEL_TEXT,
    )
    context.user_data.clear()

    return ConversationHandler.END


def profile_required(func):
    """
    Декоратор, который проверяет наличие профиля пользователя перед выполнением функции

    и отправляет сообщение о необходимости его создания при отсутствии.
    """

    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        current_chat = update.effective_chat

        try:
            await api_service.get_user_profile_by_telegram_id(current_chat.id)
        except HTTPStatusError as exc:
            if exc.response.status_code == codes.NOT_FOUND:
                await update.callback_query.answer(
                    text=templates.CREATE_USER_FIRST, show_alert=True
                )
                return ConversationHandler.END
            raise exc

        return await func(update, context, *args, **kwargs)

    return wrapper
