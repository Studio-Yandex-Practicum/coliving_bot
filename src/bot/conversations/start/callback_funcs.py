from telegram import Update
from telegram.ext import ContextTypes

from conversations.start.template import WELCOME_MESSAGE_TEXT


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=WELCOME_MESSAGE_TEXT
    )
