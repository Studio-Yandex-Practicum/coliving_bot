from dataclasses import asdict

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.invitation.keyboards as keyboards
import conversations.invitation.templates as templates
from conversations.common_functions.common_funcs import profile_required
from conversations.invitation.states import States
from internal_requests import api_service
from utils.bot import safe_send_message


@profile_required
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало диалога.
    Выводим параметры коливинга, куда приглашается пользователь,
    а также кнопки Принять/Отклонить
    """
    telegram_id = int(context.matches[0].group("telegram_id"))
    host_info = await api_service.get_user_profile_by_telegram_id(telegram_id)
    coliving_info = await api_service.get_coliving_info_by_user(telegram_id)
    context.user_data["host_info"] = host_info
    context.user_data["coliving_info"] = coliving_info

    message_text = templates.CONSIDER_INVITATION_MSG
    message_text += templates.HOST_DATA.format(**asdict(host_info))
    message_text += templates.COLIVING_DATA.format(**asdict(coliving_info))

    await update.effective_message.edit_text(
        text=message_text,
        reply_markup=keyboards.CONSIDER_INVITATION,
    )
    return States.INVITATION_START


async def process_invitation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Обрабатывает решение по коливингу.
        - отправляет сообщение хозяину
        - выводит всплывающую плашку на экран приглашенному
        - в случае принятия приглашения создает прикреление в базе данных
    Параметр decision может принимать два значения - "NO" и "YES"
    """
    current_chat = update.effective_chat
    decision = int(context.matches[0].group("decision"))

    if decision == 1:
        answer_to_host = templates.YES_TO_HOST
        message_to_roommate = templates.INVITATION_YES_MSG

        await api_service.update_user_residence(
            current_chat.id, context.user_data.get("coliving_info").id
        )
    else:
        answer_to_host = templates.NO_TO_HOST
        message_to_roommate = templates.INVITATION_NO_MSG

    await _send_message_to_host(
        update,
        context,
        context.user_data.get("host_info").user,
        current_chat.id,
        answer_to_host,
    )

    await update.callback_query.answer(
        text=message_to_roommate,
        show_alert=True,
    )
    await update.effective_message.delete()

    return ConversationHandler.END


async def _send_message_to_host(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    host_id: int,
    roommate_id: int,
    message_template: str,
) -> None:
    roommate_profile = await api_service.get_user_profile_by_telegram_id(roommate_id)

    reply_to_host = f"Пользователь <b>{roommate_profile.name}</b> "
    reply_to_host += message_template
    await safe_send_message(
        context=context,
        chat_id=host_id,
        text=reply_to_host,
    )
