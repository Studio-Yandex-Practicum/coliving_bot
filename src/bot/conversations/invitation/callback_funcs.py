from dataclasses import asdict
from typing import Optional

from telegram import InlineKeyboardMarkup, InputMediaPhoto, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ContextTypes, ConversationHandler

import conversations.invitation.keyboards as keyboards
import conversations.invitation.templates as templates
from conversations.invitation.states import States
from conversations.common_functions.common_funcs import (
    add_response_prefix,
    get_visibility_choice,
    profile_required,
)
from general.validators import value_is_in_range_validator
from internal_requests import api_service
from internal_requests.entities import Coliving, Image
from internal_requests.service import ColivingNotFound
from internal_requests.entities import MatchedUser


@profile_required
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало диалога.
    Выводим параметры коливинга, куда приглашается пользователь,
    а также кнопки Принять/Отклнить
    """
    telegram_id = int(context.matches[0].group("telegram_id"))
    host_info = await api_service.get_user_profile_by_telegram_id(telegram_id)
    coliving_info = await api_service.get_coliving_info_by_user(telegram_id)
    context.user_data["host_info"] = host_info
    context.user_data["coliving_info"] = coliving_info

    message_text = templates.CONSIDER_INVITATION_MSG
    message_text += templates.HOST_DATA.format(**asdict(host_info))
    message_text += templates.COLIVING_DATA.format(**asdict(coliving_info))

    await update.effective_message.reply_text(
        text=message_text,
        reply_markup=keyboards.CONSIDER_INVITATION,
    )
    return States.INVITATION_START


async def invitation_no(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает отклоненное приглашение в коливинг.
    """
    current_chat = update.effective_chat

    if update.callback_query:
        await update.effective_message.delete()

    reply_to_host = f"Пользователь <b>{current_chat.first_name}</b> "
    reply_to_host += templates.NO_TO_HOST
    await context.bot.send_message(
        chat_id=context.user_data.get("host_info").user,
        text=reply_to_host,
        reply_markup=ReplyKeyboardRemove(),
    )

    await update.effective_chat.send_message(
        text=templates.INVITATION_NO_MSG,
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def invitation_yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает принятое приглашение в коливинг.
    """
    current_chat = update.effective_chat

    if update.callback_query:
        await update.effective_message.delete()

    await api_service.update_user_residence(
        current_chat.id,
        context.user_data.get("coliving_info").id
    )

    reply_to_host = f"Пользователь <b>{current_chat.first_name}</b> "
    reply_to_host += templates.YES_TO_HOST
    await context.bot.send_message(
        chat_id=context.user_data.get("host_info").user,
        text=reply_to_host,
        reply_markup=ReplyKeyboardRemove(),
    )
    await update.effective_chat.send_message(
        text=templates.INVITATION_YES_MSG,
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END
