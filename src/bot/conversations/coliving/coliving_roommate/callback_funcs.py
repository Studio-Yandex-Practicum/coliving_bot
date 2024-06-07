from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from conversations.coliving import buttons
from conversations.coliving.coliving_common.coliving_common import (
    get_profile_roommate,
    handle_coliving,
    unpin_handler,
)
from conversations.coliving.coliving_roommate import templates
from conversations.coliving.states import States


async def handle_coliving_roommates(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Обработка ответа: Просмотр списка соседей."""
    return await handle_coliving(
        update=update,
        context=context,
        text=templates.COLIVING_ROOMMATES,
        state=States.COLIVING_ROOMMATE,
    )


async def get_profile_roommate_admin_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Обработчик ответа: Просмотр анкеды соседа для админа"""
    return await get_profile_roommate(
        update=update,
        context=context,
        state=States.COLIVING_ROOMMATE,
        keyboard=create_keyboard_profile_roommate,
    )


async def create_keyboard_profile_roommate(telegram_id):
    """Клавиатура администрирования соседей коливинга"""
    buttons_administrations = [
        InlineKeyboardButton(
            text=buttons.BTN_PROFILE_UNPIN_FROM_COLIVING,
            callback_data=f"profile_unpin_coliving:{telegram_id}",
        ),
        InlineKeyboardButton(
            text=buttons.BTN_PROFILE_ROOMMATE_GO_BACK,
            callback_data="roommates_profiles",
        ),
    ]
    keyboard = InlineKeyboardMarkup.from_row(buttons_administrations)
    return keyboard


async def unpin_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик открепления пользователей"""
    telegram_id = int(context.match.group("telegram_id"))
    name = context.user_data["profile_info"].name
    return await unpin_handler(
        update=update,
        context=context,
        state=States.COLIVING_ROOMMATE,
        telegram_id=telegram_id,
        text=templates.CONFIRMATION_UNPIN.format(name=name),
    )
