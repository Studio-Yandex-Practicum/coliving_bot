from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from .callback_funcs import (
    handle_about_coliving,
    handle_coliving,
    handle_confirm_or_edit_profile,
    handle_edit_about_coliving,
    handle_edit_location,
    handle_edit_photo_room,
    handle_edit_price,
    handle_edit_profile_confirmation,
    handle_edit_select_room_type,
    handle_is_visible_coliving_profile,
    handle_location,
    handle_photo_room,
    handle_price,
    handle_room_type,
    handle_what_to_edit,
    start,
)
from .states import ColivingStates as states
from .templates import COLIVING_START

acquaintance_handler: ConversationHandler = ConversationHandler(
    entry_points=[CommandHandler(COLIVING_START, start)],
    states={
        states.LOCATION: [
            CallbackQueryHandler(
                callback=handle_location, pattern=r"^moscow_city"
            ),
            CallbackQueryHandler(
                callback=handle_location, pattern=r"^spb_city"
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_location,
            ),
        ],
        states.ROOM_TYPE: [
            CallbackQueryHandler(
                callback=handle_room_type, pattern=r"^bed_in_room"
            ),
            CallbackQueryHandler(
                callback=handle_room_type,
                pattern=r"^room_in_apartment",
            ),
            CallbackQueryHandler(
                callback=handle_room_type, pattern=r"^room_in_house"
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_room_type,
            ),
        ],
        states.ABOUT_ROOM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, handle_about_coliving
            ),
        ],
        states.PRICE: [
            MessageHandler(
                # filters.Regex(r'^([0-9]{4})$') & ~filters.COMMAND, price
                filters.Regex(r"^(\d*)$") & ~filters.COMMAND,
                handle_price,
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_price),
        ],
        states.PHOTO_ROOM: [
            MessageHandler(
                filters.PHOTO & ~filters.COMMAND, handle_photo_room
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_photo_room),
        ],
        states.CONFIRMATION: [
            CallbackQueryHandler(
                callback=handle_confirm_or_edit_profile, pattern=r"^confirm"
            ),
            CallbackQueryHandler(
                callback=handle_confirm_or_edit_profile,
                pattern=r"^edit_profile",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_confirm_or_edit_profile,
                # show_coliving_profile
            ),
        ],
        states.EDIT: [
            CallbackQueryHandler(
                callback=handle_what_to_edit, pattern=r"^edit_fill_again"
            ),
            CallbackQueryHandler(
                callback=handle_what_to_edit, pattern=r"^edit_room_type"
            ),
            CallbackQueryHandler(
                callback=handle_what_to_edit, pattern=r"^edit_location"
            ),
            CallbackQueryHandler(
                callback=handle_what_to_edit, pattern=r"^edit_about"
            ),
            CallbackQueryHandler(
                callback=handle_what_to_edit, pattern=r"^edit_price"
            ),
            CallbackQueryHandler(
                callback=handle_what_to_edit, pattern=r"^edit_send_photo"
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, handle_what_to_edit
            ),
        ],
        states.IS_VISIBLE: [
            CallbackQueryHandler(
                callback=handle_is_visible_coliving_profile, pattern=r"^show"
            ),
            CallbackQueryHandler(
                callback=handle_is_visible_coliving_profile, pattern=r"^hide"
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_is_visible_coliving_profile,
            ),
        ],
        states.EDIT_LOCATION: [
            CallbackQueryHandler(
                callback=handle_edit_location, pattern=r"^moscow_city"
            ),
            CallbackQueryHandler(
                callback=handle_edit_location, pattern=r"^spb_city"
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_edit_location,
            ),
        ],
        states.EDIT_ROOM_TYPE: [
            CallbackQueryHandler(
                callback=handle_edit_select_room_type, pattern=r"^bed_in_room"
            ),
            CallbackQueryHandler(
                callback=handle_edit_select_room_type,
                pattern=r"^room_in_apartment",
            ),
            CallbackQueryHandler(
                callback=handle_edit_select_room_type,
                pattern=r"^room_in_house",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_edit_select_room_type,
            ),
        ],
        states.EDIT_ABOUT_ROOM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_edit_about_coliving,
            ),
        ],
        states.EDIT_PRICE: [
            MessageHandler(
                filters.Regex(r"^(\d*)$") & ~filters.COMMAND,
                handle_edit_price,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_edit_price,
            ),
        ],
        states.EDIT_PHOTO_ROOM: [
            MessageHandler(
                filters.PHOTO & ~filters.COMMAND,
                handle_edit_photo_room,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_edit_photo_room,
            ),
        ],
        states.EDIT_CONFIRMATION: [
            CallbackQueryHandler(
                callback=handle_edit_profile_confirmation, pattern=r"^confirm"
            ),
            CallbackQueryHandler(
                callback=handle_edit_profile_confirmation,
                pattern=r"^edit_profile",
            ),
            CallbackQueryHandler(
                callback=handle_edit_profile_confirmation, pattern=r"^cancel"
            ),
            CallbackQueryHandler(
                callback=handle_edit_profile_confirmation,
                pattern=r"^continue_editing",
            ),
            # MessageHandler(filters.TEXT & ~filters.COMMAND, show_coliving_profile),
        ],
        states.COLIVING: [
            CallbackQueryHandler(
                callback=handle_coliving, pattern=r"^edit_profile"
            ),
            CallbackQueryHandler(callback=handle_coliving, pattern=r"^show"),
            CallbackQueryHandler(callback=handle_coliving, pattern=r"^hide"),
            CallbackQueryHandler(
                callback=handle_coliving, pattern=r"^roommates_profiles"
            ),
            CallbackQueryHandler(callback=handle_coliving, pattern=r"^views"),
            CallbackQueryHandler(
                callback=handle_coliving, pattern=r"^transfer_to"
            ),
            CallbackQueryHandler(
                callback=handle_coliving, pattern=r"^go_to_menu"
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_coliving),
        ],
    },
    fallbacks=[],
)
