from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler

import conversations.match_requests.buttons as buttons
import conversations.match_requests.coliving.callback_funcs as callbacks
from conversations.common_functions import common_funcs
from conversations.match_requests.coliving import states
from conversations.match_requests.coliving.keyboards import HOST_LIKE_NOTIFY
from conversations.match_requests.profile.handlers import LIKE_REGEX_PATTERN

coliving_like_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=callbacks.start,
            pattern=LIKE_REGEX_PATTERN.format(HOST_LIKE_NOTIFY),
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
