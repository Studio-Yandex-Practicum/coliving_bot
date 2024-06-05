from telegram import Update
from telegram.ext import ContextTypes

from conversations.coliving.coliving_common.coliving_common import unpin_handler
from conversations.coliving.coliving_current_user import templates
from conversations.coliving.states import States


async def unpin_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчика открепления текущего пользователя"""
    telegram_id = update.effective_chat.id
    return await unpin_handler(
        update=update,
        context=context,
        state=States.COLIVING_CURRENT_USER,
        telegram_id=telegram_id,
        text=templates.UNLINK_FROM_COLIVING,
    )
