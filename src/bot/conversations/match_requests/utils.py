from typing import Optional

from telegram.ext import ContextTypes

from conversations.match_requests import templates as templates
from utils.bot import safe_send_message


async def send_match_notifications(update, context, sender_id, receiver_id):
    like_sender_username: str = await _get_tg_username(
        context=context, telegram_id=sender_id
    )
    like_receiver_username: str = await _get_tg_username(
        context=context, telegram_id=receiver_id
    )
    await update.effective_message.edit_text(
        text=templates.NEW_MATCH_NOTIFICATION.format(username=like_sender_username)
    )
    await safe_send_message(
        context=context,
        chat_id=sender_id,
        text=templates.NEW_MATCH_NOTIFICATION.format(username=like_receiver_username),
    )


async def _get_tg_username(
    context: ContextTypes.DEFAULT_TYPE, telegram_id: int
) -> Optional[str]:
    """Возвращает username пользователя телеграм или None в случае отсутствия."""
    chat = await context.bot.get_chat(chat_id=telegram_id)
    return chat.username
