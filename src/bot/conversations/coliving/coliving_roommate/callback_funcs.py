from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from conversations.coliving import buttons
from conversations.coliving.coliving_roommate import templates
from conversations.coliving.coliving_roommate.roommates_transfer_dry import (
    handle_coliving,
)
from conversations.coliving.states import States
from conversations.common_functions.common_funcs import add_response_prefix
from conversations.profile.callback_funcs import _look_at_profile
from internal_requests import api_service


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


async def get_profile_roommate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получить анкету соседа из списка"""
    telegram_id = int(context.match.group("telegram_id"))
    profile_data = await api_service.get_user_profile_by_telegram_id(telegram_id)

    context.user_data["profile_info"] = profile_data
    await _look_at_profile(update, context, title=templates.PROFILE_ROOMMATE)

    keyboard = await create_keyboard_profile_roommate(telegram_id)
    await update.effective_message.reply_text(
        text=templates.WHAT_DO_YOU_WANT_TO_DO, reply_markup=keyboard
    )
    await update.effective_message.edit_reply_markup()
    return States.COLIVING_ROOMMATE


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
    """Открепление соседа от коливинга"""
    telegram_id = int(context.match.group("telegram_id"))
    name = context.user_data["profile_info"].name
    keyboard = await create_keyboard_confirmation(telegram_id)
    await update.effective_message.reply_text(
        text=templates.CONFIRMATION_UNPIN.format(name=name), reply_markup=keyboard
    )
    await update.effective_message.edit_reply_markup()
    return States.COLIVING_ROOMMATE


async def create_keyboard_confirmation(telegram_id):
    """Клавиатура подтверждения открепления"""
    buttons_administrations = [
        [
            InlineKeyboardButton(
                text=buttons.YES_BTN,
                callback_data=f"unpin_profile_yes:{telegram_id}",
            ),
            InlineKeyboardButton(text=buttons.NO_BTN, callback_data="unpin_profile_no"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons_administrations)
    return keyboard


@add_response_prefix(custom_answer=buttons.YES_BTN)
async def unpin_profile_yes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Изменяем поле у пользователя residence = null"""
    telegram_id = int(context.match.group("telegram_id"))
    name = context.user_data["profile_info"].name
    await api_service.update_user_residence(telegram_id)
    await update.effective_message.reply_text(
        text=templates.ROOMMATE_NOT_IN_COLIVING_NOW.format(name=name)
    )


@add_response_prefix(custom_answer=buttons.NO_BTN)
async def unpin_profile_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выводим сообщение, что ничего не изменилось"""
    await update.effective_message.reply_text(text=templates.NOTHING_EDIT_IN_COLIVING)
