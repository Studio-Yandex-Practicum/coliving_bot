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

# from conversations.common_functions import common_buttons
from conversations.roommate_search.buttons import SEE_PROFILE

# from conversations.roommate_search.buttons import AGE_RANGE_CALLBACK_PATTERN
from conversations.roommate_search.validators import (
    handle_text_input_instead_of_choosing_button,
)

match_requests_handler: ConversationHandler = ConversationHandler(
    entry_points=[CallbackQueryHandler(callbacks.start, rf"^{SEE_PROFILE}$")],
    states={
        states.PROFILE: [
            MessageHandler(
                filters=filters.Regex(rf"^{buttons.LIKE_BTN}$"),
                callback=callbacks.link_sender_to_reciver,
            ),
            MessageHandler(
                filters=filters.Regex(rf"^{buttons.DISLIKE_BTN}$"),
                callback=callbacks.dislike_to_sender,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
    },
    fallbacks=[CommandHandler("cancel", callbacks.end_of_search)],
)
