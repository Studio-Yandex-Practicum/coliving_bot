from telegram.ext import ContextTypes

from conversations.match_requests import templates as templates
from internal_requests import api_service
from utils.bot import safe_send_message


async def send_match_notifications(update, context, sender_id, receiver_id):
    like_sender_username: str = await _get_username_or_profile_link(
        context=context, telegram_id=sender_id
    )
    like_receiver_username: str = await _get_username_or_profile_link(
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


async def _get_username_or_profile_link(
    context: ContextTypes.DEFAULT_TYPE, telegram_id: int
) -> str:
    """
    Возвращает username пользователя телеграм, если отсутствует first_name, иначе tg_id.
    """
    chat = await context.bot.get_chat(chat_id=telegram_id)
    if chat.username:
        return f"@{chat.username}"
    if chat.first_name:
        return f'<a href="tg://user?id={telegram_id}">@{chat.first_name}</a>'
    profile = await api_service.get_user_profile_by_telegram_id(telegram_id=telegram_id)
    return f'<a href="tg://user?id={telegram_id}">@{profile.name}</a>'
