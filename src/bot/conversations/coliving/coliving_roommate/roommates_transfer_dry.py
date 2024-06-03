from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ContextTypes, ConversationHandler

import conversations.coliving.coliving_transfer.templates as templates
from internal_requests import api_service


async def handle_coliving(
    update: Update, context: ContextTypes.DEFAULT_TYPE, text, state
) -> int:
    """Список пользователей коливинга"""
    page = 1
    response_json = await get_coliving_roommates_response(update, context, page)
    if response_json is None:
        context.user_data.clear()
        return ConversationHandler.END
    keyboard = await create_page_keyboard(response_json, page)
    await update.effective_message.reply_text(text=text, reply_markup=keyboard)
    await update.effective_message.edit_reply_markup()
    return state


async def get_coliving_roommates_response(
    update: Update, context: CallbackContext, page: int
) -> Optional[dict]:
    """Получение пользователей коливинга."""
    response_json = await api_service.get_coliving_roommates(
        context.user_data["coliving_info"].id, page=page
    )
    if not response_json["results"]:
        await update.effective_message.edit_reply_markup()
        await update.effective_message.reply_text(templates.EMPTY_USER_LIST_MESSAGE)
        return None
    return response_json


async def coliving_transfer_page_callback_handler(
    update: Update, context: CallbackContext
):
    """Обработка ответа перехода по страницам списка пользователей коливинга"""
    page = int(context.matches[0].group("page"))
    response_json = await get_coliving_roommates_response(update, context, page)
    if response_json is None:
        await context.user_data.clear()
        return ConversationHandler.END
    keyboard = await create_page_keyboard(response_json, page)
    await update.effective_message.edit_reply_markup(reply_markup=keyboard)
    return None


async def create_page_keyboard(response_json, page):
    """Клавиатура выбора пользователя."""
    user_buttons = []
    for user in response_json["results"]:
        user_buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{user['name']}, {user['age']}",
                    callback_data=f"profile:{user['telegram_id']}",
                )
            ]
        )
    pagination_buttons = []
    if response_json["previous"]:
        pagination_buttons.append(
            InlineKeyboardButton(text="◀️", callback_data=f"coliving_page:{page - 1}")
        )
    if response_json["next"]:
        pagination_buttons.append(
            InlineKeyboardButton(text="▶️", callback_data=f"coliving_page:{page + 1}")
        )
    user_buttons.append(pagination_buttons)
    keyboard = InlineKeyboardMarkup(inline_keyboard=user_buttons)
    return keyboard
