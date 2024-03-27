from telegram.ext import (
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import conversations.coliving.callback_funcs as callback_funcs
import conversations.coliving.templates as templates
import conversations.common_functions.common_buttons as common_buttons
import conversations.common_functions.common_funcs as common_funcs
from conversations.coliving.states import States
from conversations.common_functions.common_templates import CANCEL_TEXT
from conversations.menu.buttons import COLIVING_BUTTON

coliving_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            pattern=rf"^{COLIVING_BUTTON}$", callback=callback_funcs.start
        ),
    ],
    states={
        States.LOCATION: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_location,
                pattern=common_buttons.LOCATION_CALLBACK_PATTERN,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_location_text_input_instead_of_choosing_button,
            ),
        ],
        States.ROOM_TYPE: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_room_type,
                pattern=common_buttons.ROOM_TYPE_CALLBACK_PATTERN,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_room_type_text_input_instead_of_choosing_button,
            ),
        ],
        States.ABOUT_ROOM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, callback_funcs.handle_about_coliving
            ),
        ],
        States.PRICE: [
            MessageHandler(
                filters.Regex(r"^(\d*)$") & ~filters.COMMAND,
                callback_funcs.handle_price,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, callback_funcs.handle_price
            ),
        ],
        States.PHOTO_ROOM: [
            MessageHandler(
                filters.PHOTO | filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_photo_room,
            ),
            CallbackQueryHandler(
                pattern=rf"^{templates.SAVE_PHOTO_BUTTON}",
                callback=callback_funcs.send_received_room_photos,
            ),
        ],
        States.CONFIRMATION: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_confirm_or_edit_reply_confirm,
                pattern=rf"^{templates.BTN_LABEL_CONFIRM}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_profile_confirmation_cancel,
                pattern=rf"^{templates.BTN_LABEL_CANCEL_CREATE}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_confirm_or_cancel_profile_text_instead_of_button,
            ),
        ],
        States.EDIT: [
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
        States.IS_VISIBLE: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_is_visible_coliving_profile_yes,
                pattern=r"^is_visible:(True|False)$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.repeat_question_about_coliving_visibility,
            ),
        ],
        States.EDIT_LOCATION: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_edit_location,
                pattern=common_buttons.LOCATION_CALLBACK_PATTERN,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_location_text_input_instead_of_choosing_button,
            ),
        ],
        States.EDIT_ROOM_TYPE: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_edit_select_room_type,
                pattern=common_buttons.ROOM_TYPE_CALLBACK_PATTERN,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_room_type_text_input_instead_of_choosing_button,
            ),
        ],
        States.EDIT_ABOUT_ROOM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_edit_about_coliving,
            ),
        ],
        States.EDIT_PRICE: [
            MessageHandler(
                filters.Regex(r"^(\d*)$") & ~filters.COMMAND,
                callback_funcs.handle_edit_price,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_edit_price,
            ),
        ],
        States.EDIT_PHOTO_ROOM: [
            MessageHandler(
                filters.PHOTO,
                callback_funcs.handle_edit_photo_room,
            ),
            CallbackQueryHandler(
                pattern=rf"^{templates.SAVE_EDITED_PHOTO_BUTTON}",
                callback=callback_funcs.send_edited_room_photos,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_edit_photo_room,
            ),
        ],
        States.EDIT_CONFIRMATION: [
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
        States.COLIVING: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_coliving_edit,
                pattern=rf"^{templates.BTN_LABEL_EDIT_PROFILE_KEYBOARD}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_is_visible_switching,
                pattern=r"^is_visible:(True|False)$",
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
            CallbackQueryHandler(
                callback=callback_funcs.handle_return_to_menu_response,
                pattern=r"^go_to_menu",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                callback_funcs.handle_coliving_text_instead_of_button,
            ),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            pattern=rf"^{CANCEL_TEXT}",
            callback=common_funcs.cancel,
        ),
    ],
)

# fallbacks=[
#     CallbackQueryHandler(
#         callback=common_funcs.cancel,
#         pattern=rf"^{common_buttons.CANCEL_BUTTON}",
#     ),
# ],
# )
