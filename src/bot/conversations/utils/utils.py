from telegram import Update

from internal_requests import api_service


async def check_user_ban(update: Update):
    telegram_id = update.effective_chat.id
    user_info = await api_service.get_user_profile_by_telegram_id(
        telegram_id=telegram_id
    )
    return user_info.is_banned
