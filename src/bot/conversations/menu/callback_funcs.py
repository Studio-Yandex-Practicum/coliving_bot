from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from .keyboards import MENU_KEYBOARD
from .templates import MENU_TEXT, WELCOME_MESSAGE


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало диалога. Пиветствует пользователя.
    Предлагает посмотреть меню.
    """
    await update.effective_message.reply_text(
            text=WELCOME_MESSAGE,
    )

    return ConversationHandler.END


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Просмотр меню.
    """
    await update.effective_message.reply_text(
        text=MENU_TEXT,
        reply_markup=MENU_KEYBOARD,
    )

    return ConversationHandler.END
