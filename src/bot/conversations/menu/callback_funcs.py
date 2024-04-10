from telegram import Update
from telegram.ext import ContextTypes

from conversations.menu.keyboards import MENU_KEYBOARD
from conversations.menu.templates import MENU_TEXT, WELCOME_MESSAGE_TEXT


async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_message(
        text=WELCOME_MESSAGE_TEXT,
    )


async def menu(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """
    Просмотр меню.
    """
    await update.effective_chat.send_message(
        text=MENU_TEXT,
        reply_markup=MENU_KEYBOARD,
    )
