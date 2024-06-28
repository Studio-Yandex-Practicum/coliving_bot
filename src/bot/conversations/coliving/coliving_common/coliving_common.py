from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ContextTypes, ConversationHandler

from conversations.coliving import buttons
from conversations.coliving.coliving_current_user import templates as temp_cu
from conversations.coliving.coliving_roommate import templates as temp_room
from conversations.coliving.coliving_transfer import templates as temp_transfer
from conversations.coliving.states import States
from conversations.common_functions.common_funcs import add_response_prefix
from conversations.profile.callback_funcs import _look_at_profile
from internal_requests import api_service


async def unpin_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE, state: States, telegram_id, text
):
    """Обработчик открепления жильцов от коливинга"""
    keyboard = await create_keyboard_confirmation(telegram_id)
    if update.effective_chat.id == telegram_id:
        await update.effective_message.reply_text(text=text, reply_markup=keyboard)
    else:
        name = context.user_data["profile_info"].name
        await update.effective_message.reply_text(
            text=text.format(name=name), reply_markup=keyboard
        )
    await update.effective_message.edit_reply_markup()
    return state


async def create_keyboard_confirmation(telegram_id):
    """Клавиатура подтверждения открепления"""
    buttons_administrations = [
        InlineKeyboardButton(
            text=buttons.YES_BTN,
            callback_data=f"unpin_profile_yes:{telegram_id}",
        ),
        InlineKeyboardButton(text=buttons.NO_BTN, callback_data="unpin_profile_no"),
    ]
    keyboard = InlineKeyboardMarkup.from_row(buttons_administrations)
    return keyboard


@add_response_prefix(custom_answer=buttons.YES_BTN)
async def unpin_profile_yes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Изменяем поле у пользователя residence = null"""
    telegram_id = int(context.match.group("telegram_id"))
    await api_service.update_user_residence(telegram_id)
    if update.effective_chat.id == telegram_id:
        await update.effective_message.reply_text(text=temp_cu.YOU_UNPIN)
    else:
        name = context.user_data["profile_info"].name
        await update.effective_message.reply_text(
            text=temp_room.ROOMMATE_NOT_IN_COLIVING_NOW.format(name=name)
        )


@add_response_prefix(custom_answer=buttons.NO_BTN)
async def unpin_profile_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выводим сообщение, что ничего не изменилось"""
    await update.effective_message.reply_text(text=temp_room.NOTHING_EDIT_IN_COLIVING)


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
        await update.effective_message.reply_text(temp_transfer.EMPTY_USER_LIST_MESSAGE)
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


async def get_profile_roommate(
    update: Update, context: ContextTypes.DEFAULT_TYPE, state, keyboard
):
    """Получить анкету соседа из списка"""
    telegram_id = int(context.match.group("telegram_id"))
    profile_data = await api_service.get_user_profile_by_telegram_id(telegram_id)

    context.user_data["profile_info"] = profile_data
    await _look_at_profile(update, context, title=temp_room.PROFILE_ROOMMATE)

    keyboard = await keyboard(telegram_id)
    await update.effective_message.reply_text(
        text=temp_room.WHAT_DO_YOU_WANT_TO_DO, reply_markup=keyboard
    )
    await update.effective_message.edit_reply_markup()
    return state
