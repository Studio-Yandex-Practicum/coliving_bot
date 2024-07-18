from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import conversations.roommate_search.buttons as buttons
import conversations.roommate_search.callback_funcs as callbacks
from conversations.common_functions import common_buttons, common_funcs
from conversations.menu.buttons import SEARCH_NEIGHBOR_BUTTON
from conversations.menu.constants import CANCEL_COMMAND, MENU_COMMAND
from conversations.profile.constants import AGE_PATTERN
from conversations.roommate_search.states import States
from conversations.roommate_search.validators import (
    handle_text_input_instead_of_choosing_button,
)

roommate_search_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callbacks.start, rf"^{SEARCH_NEIGHBOR_BUTTON}$")
    ],
    states={
        States.AGE_MIN: [
            MessageHandler(
                callback=callbacks.handle_age_min_text_response,
                filters=filters.Regex(AGE_PATTERN),
            ),
            CallbackQueryHandler(
                callback=callbacks.handle_age_min_button_response,
                pattern=buttons.ANY_AGE_BTN,
            ),
            MessageHandler(
                callback=callbacks.handle_wrong_age,
                filters=~filters.COMMAND & filters.TEXT,
            ),
        ],
        States.AGE_MAX: [
            MessageHandler(
                callback=callbacks.handle_age_max_text_response,
                filters=filters.Regex(AGE_PATTERN),
            ),
            CallbackQueryHandler(
                callback=callbacks.handle_age_max_button_response,
                pattern=buttons.ANY_AGE_BTN,
            ),
            MessageHandler(
                callback=callbacks.handle_wrong_age,
                filters=~filters.COMMAND & filters.TEXT,
            ),
        ],
        States.LOCATION: [
            CallbackQueryHandler(
                callback=callbacks.set_location,
                pattern=common_buttons.LOCATION_CALLBACK_PATTERN,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.NO_MATCHES: [
            CallbackQueryHandler(
                callback=callbacks.end_of_search,
                pattern=rf"^{buttons.WAIT_BTN}$",
            ),
            CallbackQueryHandler(
                callback=callbacks.edit_settings,
                pattern=rf"^{buttons.EDIT_SETTINGS_BTN}$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.PROFILE: [
            MessageHandler(
                filters=filters.Regex(rf"^{buttons.LIKE_BTN}$"),
                callback=callbacks.profile_like,
            ),
            MessageHandler(
                filters=filters.Regex(rf"^{buttons.DISLIKE_BTN}$"),
                callback=callbacks.profile_dislike,
            ),
        ],
        States.SEX: [
            CallbackQueryHandler(
                callback=callbacks.set_sex,
                pattern=(
                    rf"^({buttons.MALE_BTN}"
                    f"|{buttons.FEMALE_BTN}"
                    f"|{buttons.ANY_GENDER_BTN})$"
                ),
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.SEARCH_SETTINGS: [
            CallbackQueryHandler(
                callback=callbacks.ok_settings,
                pattern=rf"^{buttons.OK_SETTINGS_BTN}$",
            ),
            CallbackQueryHandler(
                callback=callbacks.edit_settings,
                pattern=rf"^{buttons.EDIT_SETTINGS_BTN}$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
    },
    fallbacks=[
        CommandHandler(command=CANCEL_COMMAND, callback=common_funcs.cancel),
        CommandHandler(
            command=MENU_COMMAND,
            callback=common_funcs.return_to_menu_via_menu_command,
        ),
    ],
)
