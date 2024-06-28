from functools import wraps

from httpx import HTTPStatusError, codes
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.common_functions.common_templates as templates
from conversations.common_functions.common_buttons import (
    HIDE_SEARCH_BUTTON,
    SHOW_SEARCH_BUTTON,
)
from conversations.menu.callback_funcs import menu
from internal_requests import api_service


def add_response_prefix(custom_answer: str = ""):
    """
    Декоратор для отправки сообщения пользователю в следующем формате:
    'Твой ответ: <текст выбранной кнопки>'
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(update, context, *args, **kwargs):
            await update.effective_message.edit_reply_markup()

            if update.callback_query:
                if custom_answer:
                    user_answer = custom_answer
                else:
                    user_answer = update.callback_query.data
                    if ":" in user_answer:
                        user_answer = user_answer.split(":")[1]
                response_text = f"{templates.RESPONSE_PREFIX}{user_answer}"
                await update.effective_chat.send_message(text=response_text)
            return await func(update, context, *args, **kwargs)

        return wrapper

    return decorator


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


async def return_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Возврат в меню."""
    context.user_data.clear()

    await menu(update, context)
    return ConversationHandler.END


handle_return_to_menu_response = add_response_prefix()(return_to_menu)

return_to_menu_via_menu_command = return_to_menu
