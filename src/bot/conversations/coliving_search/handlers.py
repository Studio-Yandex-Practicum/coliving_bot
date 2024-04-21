from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import conversations.coliving_search.buttons as buttons
import conversations.coliving_search.callback_funcs as callbacks
import conversations.coliving_search.states as states
import conversations.common_functions.common_buttons as common_buttons
import conversations.common_functions.common_funcs as common_funcs
from conversations.coliving_search.validators import (
    handle_text_input_instead_of_choosing_button,
)
from conversations.menu.buttons import SEARCH_COLIVING_BUTTON
from conversations.menu.constants import CANCEL_COMMAND, MENU_COMMAND

coliving_search_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callbacks.start, rf"^{SEARCH_COLIVING_BUTTON}$")
    ],
    states={
        states.ROOM_TYPE: [
            CallbackQueryHandler(
                callback=callbacks.set_room_type,
                pattern=rf"^({buttons.TYPE_ROOM_BTN}|{buttons.TYPE_BED_BTN})$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.COST_MIN: [
            MessageHandler(
                filters.Regex(r"^(\d*)$") & ~filters.COMMAND,
                callbacks.set_cost_min,
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, callbacks.set_cost_min),
        ],
        states.COST_MAX: [
            MessageHandler(
                filters.Regex(r"^(\d*)$") & ~filters.COMMAND,
                callbacks.set_cost_max,
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, callbacks.set_cost_max),
        ],
        states.LOCATION: [
            CallbackQueryHandler(
                callback=callbacks.set_location,
                pattern=common_buttons.LOCATION_CALLBACK_PATTERN,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.NEXT_COLIVING: [
            CallbackQueryHandler(
                callback=callbacks.next_coliving,
                pattern=rf"^{buttons.YES_BTN}$",
            ),
            CallbackQueryHandler(
                callback=common_funcs.handle_return_to_menu_response,
                pattern=rf"^{common_buttons.RETURN_TO_MENU_BTN}$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.NO_MATCHES: [
            CallbackQueryHandler(
                callback=common_funcs.handle_return_to_menu_response,
                pattern=rf"^{common_buttons.RETURN_TO_MENU_BTN}$",
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
        states.COLIVING: [
            MessageHandler(
                filters=filters.Regex(rf"^{buttons.LIKE_BTN}$"),
                callback=callbacks.coliving_like,
            ),
            MessageHandler(
                filters=filters.Regex(rf"^{buttons.DISLIKE_BTN}$"),
                callback=callbacks.next_coliving,
            ),
            MessageHandler(
                filters=filters.Regex(rf"^{common_buttons.RETURN_TO_MENU_BTN}$"),
                callback=common_funcs.handle_return_to_menu_response,
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
            CallbackQueryHandler(
                callback=common_funcs.handle_return_to_menu_response,
                pattern=rf"^{common_buttons.RETURN_TO_MENU_BTN}$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
    },
    fallbacks=[
        CommandHandler(
            command=CANCEL_COMMAND,
            callback=common_funcs.cancel,
        ),
        CommandHandler(
            command=MENU_COMMAND,
            callback=common_funcs.return_to_menu_via_menu_command,
        ),
    ],
)
