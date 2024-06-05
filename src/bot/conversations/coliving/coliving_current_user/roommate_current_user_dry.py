from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from conversations.coliving import buttons
from conversations.coliving.coliving_current_user import templates as temp_cu
from conversations.coliving.coliving_roommate import templates as temp_room
from conversations.coliving.states import States
from conversations.common_functions.common_funcs import add_response_prefix
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
