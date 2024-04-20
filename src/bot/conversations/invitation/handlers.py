from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

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
                callback=callback_funcs.process_invitation,
                pattern=r"^decision_on_invitation:(?P<decision>\d+)",
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
