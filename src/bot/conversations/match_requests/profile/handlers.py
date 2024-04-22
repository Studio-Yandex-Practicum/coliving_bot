from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler

import conversations.match_requests.buttons as buttons
import conversations.match_requests.profile.callback_funcs as callbacks
import conversations.match_requests.profile.states as states
from conversations.common_functions import common_funcs
from conversations.match_requests.constants import (
    LIKE_ID_REGEX_GROUP,
    SENDER_ID_REGEX_GROUP,
)

LIKE_REGEX_PATTERN = (
    rf"^(?P<{LIKE_ID_REGEX_GROUP}>\d+)" rf":(?P<{SENDER_ID_REGEX_GROUP}>\d+)" r":{}$"
)

profile_like_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=callbacks.start,
            pattern=LIKE_REGEX_PATTERN.format(buttons.SEE_PROFILE_BNT),
        )
    ],
    states={
        states.PROFILE: [
            CallbackQueryHandler(
                callback=callbacks.link_sender_to_receiver,
                pattern=LIKE_REGEX_PATTERN.format(buttons.LIKE_BTN),
            ),
            CallbackQueryHandler(
                callback=callbacks.dislike_to_sender,
                pattern=LIKE_REGEX_PATTERN.format(buttons.DISLIKE_BTN),
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
