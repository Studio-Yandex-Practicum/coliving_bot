from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import conversations.invitation.buttons as buttons


CONSIDER_INVITATION = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=buttons.YES_INVITATION_BTN, callback_data=buttons.YES_INVITATION_BTN
        ),
        InlineKeyboardButton(
            text=buttons.NO_INVITATION_BTN, callback_data=buttons.NO_INVITATION_BTN
        ),
    )
)
