from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from conversations.coliving import buttons
from conversations.coliving.coliving_common.coliving_common import (
    get_profile_roommate,
    handle_coliving,
    unpin_handler,
)
from conversations.coliving.coliving_current_user import templates
from conversations.coliving.states import States


async def unpin_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчика открепления текущего пользователя"""
    telegram_id = update.effective_chat.id
    return await unpin_handler(
        update=update,
        context=context,
        state=States.COLIVING_CURRENT_USER,
        telegram_id=telegram_id,
        text=templates.UNLINK_FROM_COLIVING,
    )


async def current_user_roommates_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Обработчик ответа: соседи текущего пользователя"""
    return await handle_coliving(
        update=update,
        context=context,
        text=templates.YOUR_ROMMATES,
        state=States.COLIVING_CURRENT_USER,
    )


async def get_profile_roommate_cur_user_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Обработчик ответа: Просмотр анкеды соседа для текущего пользователя"""
    return await get_profile_roommate(
        update=update,
        context=context,
        state=States.COLIVING_CURRENT_USER,
        keyboard=keyboard_roommate_current_user,
    )


async def keyboard_roommate_current_user(telegram_id):
    """Клавиатура просмотра соседа по коливингу"""
    buttons_administrations = [
        InlineKeyboardButton(
            text=buttons.BTN_PROFILE_ROOMMATE_GO_BACK,
            callback_data="roommates_profiles",
        ),
    ]
    keyboard = InlineKeyboardMarkup.from_row(buttons_administrations)
    return keyboard
