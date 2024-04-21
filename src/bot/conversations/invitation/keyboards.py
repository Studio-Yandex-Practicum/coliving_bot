from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import conversations.invitation.buttons as buttons

CONSIDER_INVITATION = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=buttons.YES_INVITATION_BTN,
            callback_data="decision_on_invitation:1",
        ),
        InlineKeyboardButton(
            text=buttons.NO_INVITATION_BTN,
            callback_data="decision_on_invitation:0",
        ),
    )
)
