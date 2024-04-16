from dataclasses import asdict

from telegram import InputMediaPhoto, Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.match_requests.keyboards as keyboards
import conversations.match_requests.states as states
import conversations.match_requests.templates as templates
from conversations.common_functions.common_funcs import add_response_prefix
from conversations.match_requests.constants import MatchStatus
from conversations.roommate_search.templates import PROFILE_DATA
from internal_requests import api_service
from internal_requests.entities import UserProfile


@add_response_prefix
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало ветви по одобрению соседа.
    Проверяем, одобрен ли переход к профилу (sender)
    Вычисляем пользователя, полуившего лайк (reciver)
    Переходим к шагу показа анкеты (sender)

    """

    callback_data = update.callback_query.data
    like_sender_id, _ = callback_data.split(":")

    await show_sender_profile(
        update=update,
        like_sender_id=like_sender_id,
    )

    return states.PROFILE


async def show_sender_profile(
    update: Update,
    like_sender_id: int,
) -> int:
    """
    Отправляем сообщение с профилем отправителя
    лайка получателю
    (send sender_profile to receiver):
    - находим анкету
    - отправляем анету отправителя лайка получателю
    """

    like_sender_profile: UserProfile = (
        await api_service.get_user_profile_by_telegram_id(telegram_id=like_sender_id)
    )

    await update.effective_chat.send_message(
        text=templates.LIKE_SENDER_PROFILE.format(sender_profile=like_sender_profile)
    )

    await send_profile_info(
        update=update,
        profile=like_sender_profile,
        profile_template=PROFILE_DATA,
    )

    like_or_dislike_keyboard = await keyboards.get_like_or_dislike_keyboard(
        like_sender_id
    )
    await update.effective_chat.send_message(
        text="Что ты хочешь сделать?",
        reply_markup=like_or_dislike_keyboard,
    )
    return like_sender_profile


async def send_profile_info(
    update: Update,
    profile: UserProfile,
    profile_template: str,
):
    profile_dict: dict = asdict(profile)

    images = profile_dict.pop("images", None)
    profile_brief_info = profile_template.format(**profile_dict)

    if images:
        media_group = [InputMediaPhoto(file_id) for file_id in images]
        await update.effective_chat.send_media_group(
            media=media_group,
            caption=profile_brief_info,
        )
    else:
        await update.effective_chat.send_message(
            text=profile_brief_info,
        )


@add_response_prefix
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

    callback_data = update.callback_query.data

    like_sender_id, _ = callback_data.split(":")

    await api_service.update_match_request_status(
        sender=like_sender_id,
        receiver=like_receiver_id,
        status=MatchStatus.IS_MATCH.value,
    )

    await _send_new_match_notification(
        context=context,
        matched_user_1_tg_id=like_receiver_id,
        matched_user_2_tg_id=like_sender_id,
    )

    await _send_new_match_notification(
        context=context,
        matched_user_1_tg_id=like_sender_id,
        matched_user_2_tg_id=like_receiver_id,
    )

    return ConversationHandler.END


async def dislike_to_sender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает ДИЗЛАЙК на профиль Sender.
    Потом придумаем, как быть в таком случае
    """
    pass


async def _send_new_match_notification(
    context: ContextTypes.DEFAULT_TYPE,
    matched_user_1_tg_id: int,
    matched_user_2_tg_id: int,
):
    """
    Отправляет одному из пользовтелей пары MatchRequest со статусом is_match
    уведомление c именем второго пользователя.

    """
    #  profile: UserProfile = await api_service.get_user_profile_by_telegram_id(
    #    telegram_id=matched_user_1_tg_id,
    #  )

    chat = await context.bot.get_chat(chat_id=matched_user_1_tg_id)
    await context.bot.send_message(
        chat_id=matched_user_2_tg_id,
        text=templates.NEW_MATCH_NOTIFICATION.format(username=chat.username),
    )
