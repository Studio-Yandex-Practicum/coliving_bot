from typing import Optional

from telegram.error import Forbidden
from telegram.ext import ContextTypes

from conversations.match_requests import templates as templates
from internal_requests import api_service


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
    try:
        await context.bot.send_message(
            chat_id=sender_id,
            text=templates.NEW_MATCH_NOTIFICATION.format(
                username=like_receiver_username
            ),
        )
    except Forbidden:
        api_service.delete_profile(sender_id)


async def _get_tg_username(
    context: ContextTypes.DEFAULT_TYPE, telegram_id: int
) -> Optional[str]:
    """Возвращает username пользователя телеграм или None в случае отсутствия."""
    chat = await context.bot.get_chat(chat_id=telegram_id)
    return chat.username
