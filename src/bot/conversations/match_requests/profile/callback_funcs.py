from typing import Optional, Tuple

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.match_requests.profile.states as states
import conversations.match_requests.templates as templates
from conversations.match_requests.constants import (
    LIKE_ID_REGEX_GROUP,
    SENDER_ID_REGEX_GROUP,
    MatchStatus,
)
from conversations.match_requests.keyboards import get_like_or_dislike_keyboard
from conversations.match_requests.utils import send_match_notifications
from conversations.profile.templates import SHORT_PROFILE_DATA
from conversations.roommate_search.callback_funcs import send_profile_info
from internal_requests import api_service
from internal_requests.entities import UserProfile


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало ветви по одобрению соседа.
    Проверяем, одобрен ли переход к профилу (sender)
    Вычисляем пользователя, полуившего лайк (reciver)
    Переходим к шагу показа анкеты (sender)

    """
    like_id, sender_id = await _get_like_id_and_sender_id(context=context)

    await update.effective_message.edit_text(templates.NEIGHBOR_WANTS_TO_BE)
    await show_sender_profile(update=update, like_id=like_id, like_sender_id=sender_id)

    return states.PROFILE


async def show_sender_profile(update: Update, like_id: int, like_sender_id: int):
    """
    Находит UserProfile отправителя лайка (like_sender).
    Отправляет получателю лайка (like_receiver)
    анкету отправителя лайка (like_sender).

    """
    like_sender_profile: UserProfile = (
        await api_service.get_user_profile_by_telegram_id(telegram_id=like_sender_id)
    )

    like_or_dislike_keyboard = await get_like_or_dislike_keyboard(
        like_id=like_id,
        telegram_id=like_sender_id,
    )
    await send_profile_info(
        update=update,
        profile=like_sender_profile,
        profile_template=SHORT_PROFILE_DATA,
    )

    await update.effective_chat.send_message(
        text=templates.ASK_RESPOND_TO_LIKE,
        reply_markup=like_or_dislike_keyboard,
    )


async def link_sender_to_receiver(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Обрабатывает ЛАЙК на профиль Sender.
    Посылает запрос в API на изменение
    MatchRequest.status=is_matched,
    отправляет уведомление Sender с контактами Receiver,
    отправляет уведомление Receiver с контактами Sender
    и переводит в состояние завершения поиска.

    """
    like_receiver_id: int = update.effective_chat.id

    like_id, sender_id = await _get_like_id_and_sender_id(context=context)

    await api_service.update_status_profile_like(
        pk=like_id,
        status=MatchStatus.IS_MATCH.value,
    )

    await send_match_notifications(update, context, sender_id, like_receiver_id)
    return ConversationHandler.END


async def dislike_to_sender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает ДИЗЛАЙК на профиль Sender. Изменяет статус MatchRequest на is_rejected.
    """
    like_id, sender_id = await _get_like_id_and_sender_id(context=context)
    like_sender_profile = await api_service.get_user_profile_by_telegram_id(
        telegram_id=sender_id
    )

    await api_service.update_status_profile_like(
        pk=like_id,
        status=MatchStatus.IS_REJECTED.value,
    )

    await update.effective_message.edit_text(
        text=templates.REJECTION_NOTIFICATION.format(sender_profile=like_sender_profile)
    )


async def _get_like_id_and_sender_id(
    context: ContextTypes.DEFAULT_TYPE,
) -> Tuple[int, int]:
    """Возвращает id ProfileLike для дальнейшего формирования запроса к API."""
    like_id: int = int(context.matches[0].group(LIKE_ID_REGEX_GROUP))
    sender_id: int = int(context.matches[0].group(SENDER_ID_REGEX_GROUP))
    return like_id, sender_id


async def _get_tg_username(
    context: ContextTypes.DEFAULT_TYPE, telegram_id: int
) -> Optional[str]:
    """Возвращает username пользователя телеграм или None в случае отсутствия."""
    chat = await context.bot.get_chat(chat_id=telegram_id)
    return chat.username
