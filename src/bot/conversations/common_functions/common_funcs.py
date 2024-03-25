from httpx import HTTPStatusError, codes
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.common_functions.common_templates as templates
from conversations.menu.callback_funcs import menu
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


async def profile_exist_check(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Проверяет, создана ли анкета пользователя
    """

    current_chat = update.effective_chat

    try:
        await api_service.get_user_profile_by_telegram_id(current_chat)
    except HTTPStatusError as exc:
        if exc.response.status_code == codes.NOT_FOUND:
            await current_chat.send_message(text=templates.CREATE_USER_FIRST)
            await menu(update, context)
            return ConversationHandler.END
        raise exc
