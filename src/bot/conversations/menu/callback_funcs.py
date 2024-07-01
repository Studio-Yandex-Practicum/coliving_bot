from telegram import Update
from telegram.ext import ContextTypes, CallbackContext

from conversations.menu.keyboards import MENU_KEYBOARD
from conversations.menu.templates import (MENU_TEXT,
                                          WELCOME_MESSAGE_TEXT,
                                          ADDITION_MESSAGE_TEXT)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_message(
        text=WELCOME_MESSAGE_TEXT,
    )
    chat_id = update.effective_chat.id
    context.job_queue.run_once(callback=send_additional_message, when=30, data=chat_id)


async def send_additional_message(context: CallbackContext) -> None:
    data = context.job.data
    await context.bot.send_message(chat_id=data, text=ADDITION_MESSAGE_TEXT)


async def menu(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """
    Просмотр меню.
    """
    await update.effective_chat.send_message(
        text=MENU_TEXT,
        reply_markup=MENU_KEYBOARD,
    )
