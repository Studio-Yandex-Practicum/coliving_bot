from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.match_requests.keyboards as keyboards
import conversations.match_requests.states as states
import conversations.match_requests.templates as templates
from conversations.common_functions.common_funcs import add_response_prefix
from conversations.match_requests.constants import TG_ID_REGEX_GRP, MatchStatus
from conversations.roommate_search.callback_funcs import send_profile_info
from conversations.roommate_search.templates import PROFILE_DATA
from internal_requests import api_service
from internal_requests.entities import UserProfile


@add_response_prefix()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало ветви по одобрению соседа.
    Проверяем, одобрен ли переход к профилу (sender)
    Вычисляем пользователя, полуившего лайк (reciver)
    Переходим к шагу показа анкеты (sender)

    """
    like_sender_id: int = await _get_like_sender_tg_id(context=context)

    await show_sender_profile(
        update=update,
        like_sender_id=like_sender_id,
    )

    return states.PROFILE


async def show_sender_profile(update: Update, like_sender_id: int):
    """
    Находит UserProfile отправителя лайка (like_sender).
    Отправляет получателю лайка (like_receiver)
    анкету отправителя лайка (like_sender).

    """
    like_sender_profile: UserProfile = (
        await api_service.get_user_profile_by_telegram_id(telegram_id=like_sender_id)
    )

    like_or_dislike_keyboard = await keyboards.get_like_or_dislike_keyboard(
        telegram_id=like_sender_id,
    )
    await send_profile_info(
        update=update,
        profile=like_sender_profile,
        profile_template=PROFILE_DATA,
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

    like_sender_id: int = await _get_like_sender_tg_id(context=context)

    await api_service.update_match_request_status(
        sender=like_sender_id,
        receiver=like_receiver_id,
        status=MatchStatus.IS_MATCH.value,
    )

    like_sender_username: str = await _get_tg_username(
        context=context, telegram_id=like_sender_id
    )
    like_receiver_username: str = await _get_tg_username(
        context=context, telegram_id=like_receiver_id
    )

    await update.effective_message.edit_text(
        text=templates.NEW_MATCH_NOTIFICATION.format(username=like_sender_username)
    )

    await context.bot.send_message(
        chat_id=like_sender_id,
        text=templates.NEW_MATCH_NOTIFICATION.format(username=like_receiver_username),
    )
    return ConversationHandler.END


async def dislike_to_sender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает ДИЗЛАЙК на профиль Sender. Изменяет статус MatchRequest на is_rejected.

    """
    like_receiver_id: int = update.effective_chat.id

    like_sender_id: int = await _get_like_sender_tg_id(context=context)
    like_sender_profile = await api_service.get_user_profile_by_telegram_id(
        telegram_id=like_sender_id
    )

    await api_service.update_match_request_status(
        sender=like_sender_id,
        receiver=like_receiver_id,
        status=MatchStatus.IS_REJECTED.value,
    )

    await update.effective_message.edit_text(
        text=templates.REJECTION_NOTIFICATION.format(sender_profile=like_sender_profile)
    )


async def _get_like_sender_tg_id(context: ContextTypes.DEFAULT_TYPE) -> int:
    """Возвращает telegram id отправителя лайка."""
    like_sender_id: int = int(context.matches[0].group(TG_ID_REGEX_GRP))
    return like_sender_id


async def _get_tg_username(
    context: ContextTypes.DEFAULT_TYPE, telegram_id: int
) -> Optional[str]:
    """Возвращает username пользователя телеграм или None в случае отсутствия."""
    chat: str = await context.bot.get_chat(chat_id=telegram_id)
    return chat.username
