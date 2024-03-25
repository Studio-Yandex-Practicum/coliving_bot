from functools import wraps

from httpx import HTTPStatusError, codes
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.common_functions.common_templates as templates
from internal_requests import api_service


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяет текущий диалог."""
    await update.effective_message.reply_text(
        text=templates.CANCEL_TEXT,
    )
    await update.effective_message.edit_reply_markup()
    context.user_data.clear()

    return ConversationHandler.END


def combine_keyboards(keyboard1, keyboard2):
    """
    Объединяет две клавиатуры типа InlineKeyboardMarkup в одну клавиатуру.

    :param keyboard1: Первая клавиатура для объединения.
    :param keyboard2: Вторая клавиатура для объединения.
    :return: Объединенная клавиатура типа InlineKeyboardMarkup.
    """
    combined_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[*keyboard1.inline_keyboard, *keyboard2.inline_keyboard]
    )

    return combined_keyboard


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
