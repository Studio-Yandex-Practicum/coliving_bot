from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

import conversations.invitation.buttons as buttons
from conversations.common_functions.common_buttons import (
    LOCATION_PREFIX,
    RETURN_TO_MENU_BTN_LABEL,
    ROOM_TYPE_PREFIX,
)
from conversations.common_functions.common_keyboards import HIDE_BUTTON, SEARCH_BUTTON
from internal_requests import api_service


CONSIDER_INVITATION = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=buttons.YES_INVITATION_BTN, callback_data=buttons.YES_INVITATION_BTN),
        InlineKeyboardButton(text=buttons.NO_INVITATION_BTN, callback_data=buttons.NO_INVITATION_BTN),
    )
)
