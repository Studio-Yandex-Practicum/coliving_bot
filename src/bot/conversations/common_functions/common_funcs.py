from functools import wraps

from httpx import HTTPStatusError, codes
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.common_functions.common_templates as templates
from conversations.common_functions.common_buttons import (
    HIDE_SEARCH_BUTTON,
    SHOW_SEARCH_BUTTON,
)
from internal_requests import api_service


def add_response_prefix(func=None, custom_message=None):
    """
    Декоратор для отправки сообщения пользователю в следующем формате:
    'Твой ответ: <текст выбранной кнопки>'
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(update, context, *args, **kwargs):
            if update.callback_query:
                user_response = update.callback_query.data
                if ":" in user_response:
                    user_response = user_response.split(":")[1]
                if custom_message:
                    response_text = custom_message
                else:
                    response_text = f"{templates.RESPONSE_PREFIX}{user_response}"
                await update.effective_chat.send_message(text=response_text)
            return await func(update, context, *args, **kwargs)

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяет текущий диалог."""
    await update.effective_message.reply_text(
        text=templates.CANCEL_TEXT,
        reply_markup=ReplyKeyboardRemove(),
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


async def get_visibility_choice(update: Update) -> bool:
    """ "
    Обрабатывает нажатие кнопок 'Показать в поиске/Скрыть из поиска'
    и возвращает True для 'Показать в поиске'
    и False для 'Скрыть из поиска'.

    """
    visibility_btn = update.callback_query.data

    visibility_options = {
        SHOW_SEARCH_BUTTON: True,
        HIDE_SEARCH_BUTTON: False,
    }

    return visibility_options[visibility_btn]
