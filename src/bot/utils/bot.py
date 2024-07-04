from typing import Optional

from telegram import InlineKeyboardMarkup
from telegram.error import Forbidden
from telegram.ext import ContextTypes

from internal_requests import api_service


async def safe_send_message(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    text: str,
    reply_markup: Optional[InlineKeyboardMarkup] = None,
):
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
        )
    except Forbidden:
        user = await api_service.get_user_profile_by_telegram_id(chat_id)
        user.is_visible = False
        await api_service.update_user_profile(user)
