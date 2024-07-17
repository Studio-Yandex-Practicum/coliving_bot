from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

import conversations.menu.templates as templates
from internal_requests import api_service

from .buttons import (
    COLIVING_BUTTON,
    MY_PROFILE_BUTTON,
    SEARCH_COLIVING_BUTTON,
    SEARCH_NEIGHBOR_BUTTON,
    USEFUL_INFO_BUTTON,
)

MENU_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=MY_PROFILE_BUTTON, callback_data=MY_PROFILE_BUTTON),
        InlineKeyboardButton(text=COLIVING_BUTTON, callback_data=COLIVING_BUTTON),
        InlineKeyboardButton(
            text=SEARCH_NEIGHBOR_BUTTON, callback_data=SEARCH_NEIGHBOR_BUTTON
        ),
        InlineKeyboardButton(
            text=SEARCH_COLIVING_BUTTON, callback_data=SEARCH_COLIVING_BUTTON
        ),
        InlineKeyboardButton(text=USEFUL_INFO_BUTTON, callback_data=USEFUL_INFO_BUTTON),
    )
)


async def get_useful_info_keyboard(
    context: ContextTypes.DEFAULT_TYPE,
) -> InlineKeyboardMarkup:
    if context.bot_data.get("useful_info") is None:
        materials = await api_service.get_useful_materials()
    else:
        materials = context.bot_data.get("useful_info")

    return InlineKeyboardMarkup.from_column(
        [
            InlineKeyboardButton(text=material.title, url=material.url)
            for material in materials
        ]
    )


def get_main_menu_commands() -> list[BotCommand]:
    """Создает кнопку с меню бота и добавляет в нее команды."""
    return [
        BotCommand(cmd, description) for cmd, description in templates.COMMANDS.items()
    ]
