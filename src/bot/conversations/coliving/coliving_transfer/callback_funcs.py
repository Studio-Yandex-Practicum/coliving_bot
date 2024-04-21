from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ContextTypes, ConversationHandler

import conversations.coliving.coliving_transfer.templates as templates
from conversations.coliving import keyboards as keyboards
from conversations.coliving.buttons import BTN_LABEL_CANCEL, BTN_LABEL_CONFIRM
from conversations.coliving.states import States
from conversations.common_functions.common_funcs import add_response_prefix
from internal_requests import api_service


async def handle_coliving_transfer_to(update, context):
    """Обработка ответа: Передача коливинга."""
    page = 1
    response_json = await _get_coliving_roommates_response(update, context, page)
    if response_json is None:
        context.user_data.clear()
        return ConversationHandler.END
    keyboard = await _create_page_keyboard(response_json, page)
    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=templates.SELECT_USER_MESSAGE, reply_markup=keyboard
    )
    return States.TRANSFER_COLIVING


async def coliving_transfer_page_callback_handler(
    update: Update, context: CallbackContext
):
    """Обработка ответа перехода по страницам при передаче коливинга."""
    page = int(context.matches[0].group("page"))
    response_json = await _get_coliving_roommates_response(update, context, page)
    if response_json is None:
        await context.user_data.clear()
        return ConversationHandler.END
    keyboard = await _create_page_keyboard(response_json, page)
    await update.effective_message.edit_reply_markup(reply_markup=keyboard)
    return None


async def handle_coliving_transfer_to_confirm(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Обработка выбора нового владельца коливинга."""
    telegram_id = int(context.matches[0].group("telegram_id"))
    user_info = await api_service.get_user_profile_by_telegram_id(telegram_id)
    context.user_data["coliving_info"].host = telegram_id
    await update.effective_message.edit_text(
        text=templates.USER_INFO_MESSAGE_TEMPLATE.format(
            name=user_info.name, age=user_info.age
        ),
        reply_markup=keyboards.COLIVING_TRANSFER_TO_CONFIRM_KEYBOARD,
    )
    return None


@add_response_prefix(custom_answer=BTN_LABEL_CONFIRM)
async def handle_coliving_set_new_owner(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Обработка выбора нового владельца коливинга."""
    await api_service.update_coliving_info(context.user_data["coliving_info"])
    await context.bot.send_message(
        chat_id=context.user_data["coliving_info"].host,
        text=templates.NEW_COLIVING_OWNER_MESSAGE,
    )
    await update.effective_message.reply_text(text=templates.OWNER_CHANGED_MESSAGE)
    return ConversationHandler.END


@add_response_prefix(custom_answer=BTN_LABEL_CANCEL)
async def handle_cancel_coliving_transfer(update: Update, _context: CallbackContext):
    """Обработка отмены передачи коливинга."""
    await update.effective_message.reply_text(templates.CANCELLATION_MESSAGE)
    return ConversationHandler.END


async def _get_coliving_roommates_response(
    update: Update, context: CallbackContext, page: int
) -> Optional[dict]:
    """Проверка наличия пользователей для передачи коливига."""
    response_json = await api_service.get_coliving_roommates(
        context.user_data["coliving_info"].id, page=page
    )
    if not response_json["results"]:
        await update.effective_message.edit_reply_markup()
        await update.effective_message.reply_text(templates.EMPTY_USER_LIST_MESSAGE)
        return None
    return response_json


async def _create_page_keyboard(response_json, page):
    """Клавиатура выбора пользователя для передачи коливинга."""
    user_buttons = []
    for user in response_json["results"]:
        user_buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{user['name']}, {user['age']}",
                    callback_data=f"transfer_to_confirm:{user['telegram_id']}",
                )
            ]
        )
    pagination_buttons = []
    if response_json["previous"]:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="◀️", callback_data=f"coliving_transfer_page:{page - 1}"
            )
        )
    if response_json["next"]:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="▶️", callback_data=f"coliving_transfer_page:{page + 1}"
            )
        )
    user_buttons.append(pagination_buttons)
    keyboard = InlineKeyboardMarkup(inline_keyboard=user_buttons)
    return keyboard
