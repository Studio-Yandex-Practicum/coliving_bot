from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import conversations.match_requests.buttons as buttons
import conversations.match_requests.callback_funcs as callbacks
import conversations.match_requests.states as states
from conversations.common_functions import common_funcs

# from conversations.roommate_search.buttons import AGE_RANGE_CALLBACK_PATTERN
from conversations.roommate_search.validators import (
    handle_text_input_instead_of_choosing_button,
)

match_requests_handler: ConversationHandler = ConversationHandler(
    # entry_points=[CallbackQueryHandler(callbacks.start, rf"^{SEE_PROFILE}$")],
    entry_points=[
        CallbackQueryHandler(
            callback=callbacks.start, pattern=rf"^\d+:{buttons.SEE_PROFILE_BNT}$"
        )
    ],
    states={
        states.PROFILE: [
            CallbackQueryHandler(
                callback=callbacks.link_sender_to_receiver,
                pattern=rf"^\d+:{buttons.LIKE_BTN}$",
            ),
            CallbackQueryHandler(
                callback=callbacks.dislike_to_sender,
                pattern=rf"^\d+:{buttons.DISLIKE_BTN}$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
    },
    fallbacks=[
        CommandHandler(
            command="cancel",
            callback=common_funcs.cancel,
        ),
    ],
)
