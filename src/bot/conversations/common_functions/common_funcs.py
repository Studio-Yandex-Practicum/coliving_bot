from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.common_functions.common_templates as templates


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
