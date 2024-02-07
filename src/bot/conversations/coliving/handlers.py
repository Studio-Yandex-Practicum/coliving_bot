from telegram.ext import (
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import conversations.coliving.callback_funcs as callback_funcs
import conversations.coliving.states as states
import conversations.coliving.templates as templates
from conversations.menu.callback_funcs import menu

coliving_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            pattern=rf"^{templates.COLIVING_START_BTN}$", callback=callback_funcs.start
        ),
    ],
    states={
        states.LOCATION: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_location,
                pattern=rf"^{templates.LOCATION_CALLBACK_DATA}:(.+)$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_location_text_input_instead_of_choosing_button,
            ),
        ],
        states.ROOM_TYPE: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_room_type,
                pattern=rf"^{templates.ROOM_TYPE_CALLBACK_DATA}:(.+)$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_room_type_text_input_instead_of_choosing_button,
            ),
        ],
        states.ABOUT_ROOM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, callback_funcs.handle_about_coliving
            ),
        ],
        states.PRICE: [
            MessageHandler(
                filters.Regex(r"^(\d*)$") & ~filters.COMMAND,
                callback_funcs.handle_price,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, callback_funcs.handle_price
            ),
        ],
        states.PHOTO_ROOM: [
            MessageHandler(
                filters.PHOTO | filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_photo_room,
            ),
        ],
        states.CONFIRMATION: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_confirm_or_edit_reply_confirm,
                pattern=rf"^{templates.BTN_LABEL_CONFIRM}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_confirm_or_edit_reply_edit_profile,
                pattern=rf"^{templates.BTN_LABEL_EDIT_PROFILE_KEYBOARD}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_confirm_or_edit_profile_text_instead_of_button,
            ),
        ],
        states.EDIT: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_what_to_edit_fill_again,
                pattern=rf"^{templates.BTN_LABEL_FILL_AGAIN}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_what_to_edit_room_type,
                pattern=rf"^{templates.BTN_LABEL_EDIT_ROOM_TYPE}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_what_to_edit_location,
                pattern=rf"^{templates.BTN_LABEL_EDIT_LOCATION}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_what_to_edit_about_room,
                pattern=rf"^{templates.BTN_LABEL_EDIT_ABOUT_ROOM}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_what_to_edit_price,
                pattern=rf"^{templates.BTN_LABEL_EDIT_PRICE}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_what_to_edit_photo_room,
                pattern=rf"^{templates.BTN_LABEL_EDIT_PHOTO}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_what_to_edit_text_instead_of_button,
            ),
        ],
        states.IS_VISIBLE: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_is_visible_coliving_profile_yes,
                pattern=r"^(True|False)$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.repeat_question_about_coliving_visibility,
            ),
        ],
        states.EDIT_LOCATION: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_edit_location,
                pattern=rf"^{templates.LOCATION_CALLBACK_DATA}:(.+)",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_location_text_input_instead_of_choosing_button,
            ),
        ],
        states.EDIT_ROOM_TYPE: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_edit_select_room_type,
                pattern=rf"^{templates.ROOM_TYPE_CALLBACK_DATA}:(.+)$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_room_type_text_input_instead_of_choosing_button,
            ),
        ],
        states.EDIT_ABOUT_ROOM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_edit_about_coliving,
            ),
        ],
        states.EDIT_PRICE: [
            MessageHandler(
                filters.Regex(r"^(\d*)$") & ~filters.COMMAND,
                callback_funcs.handle_edit_price,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_edit_price,
            ),
        ],
        states.EDIT_PHOTO_ROOM: [
            MessageHandler(
                filters.PHOTO,
                callback_funcs.handle_edit_photo_room,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_edit_photo_room,
            ),
        ],
        states.EDIT_CONFIRMATION: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_edit_profile_confirmation_confirm,
                pattern=rf"^{templates.BTN_LABEL_CONFIRM}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_edit_profile_confirmation_cancel,
                pattern=rf"^{templates.BTN_LABEL_CANCEL_EDIT}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_edit_profile_confirmation_continue_edit,
                pattern=rf"^{templates.BTN_LABEL_EDIT_CONTINUE}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_edit_profile_confirmation_text_instead_of_button,
            ),
        ],
        states.COLIVING: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_coliving_edit,
                pattern=rf"^{templates.BTN_LABEL_EDIT_PROFILE_KEYBOARD}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_is_visible_switching,
                pattern=r"^(False|True)$",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_coliving_roommates,
                pattern=r"^roommates_profiles",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_coliving_views, pattern=r"^views"
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_coliving_transfer_to,
                pattern=r"^transfer_to",
            ),
            CallbackQueryHandler(callback=menu, pattern=r"^go_to_menu"),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_coliving_text_instead_of_button,
            ),
        ],
    },
    fallbacks=[],
)
