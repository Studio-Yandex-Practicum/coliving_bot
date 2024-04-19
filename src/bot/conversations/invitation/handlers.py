from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

import conversations.invitation.buttons as buttons
import conversations.invitation.callback_funcs as callback_funcs
import conversations.common_functions.common_funcs as common_funcs
from conversations.invitation.states import States

invitation_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=callback_funcs.start,
            pattern=r"^coliving_host:(?P<telegram_id>\d+)",
        ),
    ],
    states={
        States.INVITATION_START: [
            CallbackQueryHandler(
                callback=callback_funcs.invitation_yes,
                pattern=rf"^{buttons.YES_INVITATION_BTN}$",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.invitation_no,
                pattern=rf"^{buttons.NO_INVITATION_BTN}$",
            ),
        ],
        States.INVITATION_NO: [
            CallbackQueryHandler(
                callback=callback_funcs.invitation_no,
                pattern=rf"^{buttons.NO_INVITATION_BTN}$",
            ),
        ],
        States.INVITATION_YES: [
            CallbackQueryHandler(
                callback=callback_funcs.invitation_yes,
                pattern=rf"^{buttons.YES_INVITATION_BTN}$",
            ),
        ],
    },
    fallbacks=[
        CommandHandler(
            "cancel",
            common_funcs.cancel,
        ),
    ],
)
