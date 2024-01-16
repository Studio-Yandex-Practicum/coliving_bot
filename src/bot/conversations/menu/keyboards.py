from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup

import conversations.menu.templates as templates

from .buttons import (
    COLIVING_BUTTON,
    MY_PROFILE_BUTTON,
    SEARCH_COLIVING_BUTTON,
    SEARCH_NEIGHBOR_BUTTON,
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
    )
)


def get_main_menu_commands() -> list[BotCommand]:
    """Создает кнопку с меню бота и добавляет в нее команды."""
    return [
        BotCommand(cmd, description) for cmd, description in templates.COMMANDS.items()
    ]
