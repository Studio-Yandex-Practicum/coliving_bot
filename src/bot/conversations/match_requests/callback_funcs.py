from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

# import conversations.match_requests.buttons as buttons
import conversations.match_requests.keyboards as keyboards
import conversations.match_requests.states as states
import conversations.match_requests.templates as templates
from internal_requests import api_service

# from internal_requests.entities import SearchSettings, UserProfile


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало ветви по одобрению соседа.
    Проверяем, одобрен ли переход к профайлу (sender)
    Вычисляем пользователя, полуившего лайк (reciver)
    Переходим к шагу показа анкеты (sender)
    """

    if update.callback_query:
        await update.effective_message.delete()

    sender_id = update.effective_chat.id
    callback_data = update.callback_query.data
    receiver_id = callback_data.split("_")[2]

    await show_profile(
        context,
        sender_id,
        receiver_id,
    )

    return states.PROFILE


async def show_profile(
    context: ContextTypes.DEFAULT_TYPE,
    sender_id,
    receiver_id,
) -> int:
    """
    Отправляем сообщение с профилем отправителя
    лайка получателю
    (send sender_profile to reciver):
    - находим анкету
    - отправляем анету отправителя лайка получателю
    """

    sender_profile = await api_service.get_user_profile(sender_id)

    await context.bot.send_message(
        chat_id=receiver_id,
        text=templates.SENDER_PROFILE,
        reply_markup=keyboards.PROFILE_KEYBOARD,
    )
    return sender_profile


async def link_sender_to_reciver(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает ЛАЙК на профиль Sender.
    Посылает запрос в API на изменение
    MatchRequest.status=is_matched,
    отправляет уведомление Sender с контактами Reciver,
    отправляет уведомление Reciver с контактами Sender
    и переводит в состояние завершения поиска.
    """
    current_profile = context.user_data.get("current_profile")
    sender_id = update.effective_chat.id
    receiver_id = current_profile["user"]
    status_match_request = "is_matched"
    status = status_match_request

    await api_service.change_match_request_status(
        sender_id=sender_id,
        receiver_id=receiver_id,
        status=status,
    )

    await context.bot.send_message(
        chat_id=sender_id,
        text=templates.SEND_RECIVER,
        parse_mode=ParseMode.HTML,
    )

    await context.bot.send_message(
        chat_id=receiver_id,
        text=templates.SEND_SENDER,
        parse_mode=ParseMode.HTML,
    )

    return ConversationHandler.END


async def dislike_to_sender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает ДИЗЛАЙК на профиль Sender.
    Потом придумаем, как быть в таком случае
    """
    pass
