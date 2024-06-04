from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from conversations.coliving import buttons
from conversations.coliving.coliving_current_user import templates
from conversations.coliving.states import States
from conversations.common_functions.common_funcs import add_response_prefix
from internal_requests import api_service


async def unpin_me_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Открепление текущего пользователя"""
    current_user_id = update.effective_chat.id
    keyboard = await create_keyboard_confirmation(current_user_id)
    await update.effective_message.reply_text(
        text=templates.UNLINK_FROM_COLIVING, reply_markup=keyboard
    )
    await update.effective_message.edit_reply_markup()
    return States.COLIVING_CURRENT_USER


async def create_keyboard_confirmation(telegram_id):
    """Клавиатура подтверждения открепления"""
    buttons_administrations = [
        [
            InlineKeyboardButton(
                text=buttons.YES_BTN,
                callback_data="unpin_me_yes",
            ),
            InlineKeyboardButton(text=buttons.NO_BTN, callback_data="unpin_me_no"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons_administrations)
    return keyboard


@add_response_prefix(custom_answer=buttons.YES_BTN)
async def unpin_me_yes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Изменяем поле у пользователя residence = null"""
    current_user_id = update.effective_chat.id
    await api_service.update_user_residence(current_user_id)
    await update.effective_message.reply_text(text=templates.YOU_UNPIN)


@add_response_prefix(custom_answer=buttons.NO_BTN)
async def unpin_me_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выводим сообщение, что ничего не изменилось"""
    await update.effective_message.reply_text(text=templates.NOTHING_HAPPENED)
