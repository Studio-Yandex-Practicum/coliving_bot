from typing import TypedDict

from telegram import Update
from telegram.ext import CallbackContext, ContextTypes

from conversations.menu.keyboards import MENU_KEYBOARD
from conversations.menu.templates import (
    MENU_TEXT,
    START_MESSAGE_1,
    START_MESSAGE_2,
    START_MESSAGE_3,
)


class Message(TypedDict):
    chat_id: int
    text: str


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_message(
        text=START_MESSAGE_1,
    )
    chat_id = update.effective_chat.id
    context.job_queue.run_once(
        callback=send_delayed_message,
        when=30,
        data=Message(chat_id=chat_id, text=START_MESSAGE_2),
    )
    context.job_queue.run_once(
        callback=send_delayed_message,
        when=60,
        data=Message(chat_id=chat_id, text=START_MESSAGE_3),
    )


async def send_delayed_message(context: CallbackContext) -> None:
    data = context.job.data
    if not isinstance(data, dict):
        raise TypeError("Expected data to be a dictionary")
    await context.bot.send_message(**data)


async def menu(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """
    Просмотр меню.
    """
    await update.effective_chat.send_message(
        text=MENU_TEXT,
        reply_markup=MENU_KEYBOARD,
    )
