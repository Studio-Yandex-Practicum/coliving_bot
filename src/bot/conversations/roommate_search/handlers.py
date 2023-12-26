from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import conversations.roommate_search.callback_funcs as callbacks
import conversations.roommate_search.templates as buttons

from .states import RoommateSearchStates as states
from .validators import handle_text_input_instead_of_choosing_button

roommate_search_handler: ConversationHandler = ConversationHandler(
    entry_points=[CommandHandler("roommate_search", callbacks.start)],
    states={
        states.AGE: [
            CallbackQueryHandler(
                callback=callbacks.set_age,
                pattern=rf"^({buttons.AGE_18_23_BTN}|{buttons.AGE_24_29_BTN}|"
                f"{buttons.AGE_30_35_BTN}|{buttons.AGE_36_40_BTN}|"
                f"{buttons.AGE_41_45_BTN}|{buttons.AGE_46_50_BTN}|"
                f"{buttons.AGE_51_55_BTN}|{buttons.AGE_55UP_BTN})$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.LOCATION: [
            CallbackQueryHandler(
                callback=callbacks.set_location,
                pattern=rf"^({buttons.MSK_BTN}|{buttons.SPB_BTN})$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.NEXT_PROFILE: [
            CallbackQueryHandler(
                callback=callbacks.next_profile,
                pattern=rf"^{buttons.YES_BTN}$",
            ),
            CallbackQueryHandler(
                callback=callbacks.end_of_search,
                pattern=rf"^{buttons.NO_BTN}$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.NO_MATCHES: [
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
        states.PROFILE: [
            CallbackQueryHandler(
                callback=callbacks.profile_like,
                pattern=rf"^{buttons.LIKE_BTN}$",
            ),
            CallbackQueryHandler(
                callback=callbacks.next_profile,
                pattern=rf"^{buttons.DISLIKE_BTN}$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.SEX: [
            CallbackQueryHandler(
                callback=callbacks.set_sex,
                pattern=rf"^({buttons.MALE_BTN}|{buttons.FEMALE_BTN})$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.SEARCH_SETTINGS: [
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
    fallbacks=[],
)
