from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from .callback_funcs import (
    handle_about_coliving,
    handle_coliving_edit,
    handle_coliving_go_to_menu,
    handle_coliving_hide,
    handle_coliving_roommates,
    handle_coliving_show,
    handle_coliving_text_instead_of_button,
    handle_coliving_transfer_to,
    handle_coliving_views,
    handle_confirm_or_edit_profile_text_instead_of_button,
    handle_confirm_or_edit_reply_confirm,
    handle_confirm_or_edit_reply_edit_profile,
    handle_edit_about_coliving,
    handle_edit_location,
    handle_edit_photo_room,
    handle_edit_price,
    handle_edit_profile_confirmation_cancel,
    handle_edit_profile_confirmation_confirm,
    handle_edit_profile_confirmation_continue_edit,
    handle_edit_profile_confirmation_text_instead_of_button,
    handle_edit_select_room_type,
    handle_is_visible_coliving_profile_no,
    handle_is_visible_coliving_profile_text_instead_of_button,
    handle_is_visible_coliving_profile_yes,
    handle_location,
    handle_location_text_input_instead_of_choosing_button,
    handle_photo_room,
    handle_price,
    handle_room_type,
    handle_room_type_text_input_instead_of_choosing_button,
    handle_what_to_edit_about_room,
    handle_what_to_edit_fill_again,
    handle_what_to_edit_location,
    handle_what_to_edit_photo_room,
    handle_what_to_edit_price,
    handle_what_to_edit_room_type,
    handle_what_to_edit_text_instead_of_button,
    start,
)
from .states import ColivingStates as states
from .templates import (
    BTN_LABEL_BED_IN_ROOM,
    BTN_LABEL_CANCEL_EDIT,
    BTN_LABEL_CONFIRM,
    BTN_LABEL_EDIT_ABOUT_ROOM,
    BTN_LABEL_EDIT_CONTINUE,
    BTN_LABEL_EDIT_LOCATION,
    BTN_LABEL_EDIT_PHOTO,
    BTN_LABEL_EDIT_PRICE,
    BTN_LABEL_EDIT_PROFILE_KEYBOARD,
    BTN_LABEL_EDIT_ROOM_TYPE,
    BTN_LABEL_FILL_AGAIN,
    BTN_LABEL_MOSCOW,
    BTN_LABEL_ROOM_IN_APPARTMENT,
    BTN_LABEL_ROOM_IN_HOUSE,
    BTN_LABEL_SPB,
    COLIVING_START,
)

coliving_handler: ConversationHandler = ConversationHandler(
    entry_points=[CommandHandler(COLIVING_START, start)],
    states={
        states.LOCATION: [
            CallbackQueryHandler(
                callback=handle_location, pattern=rf"^{BTN_LABEL_MOSCOW}"
            ),
            CallbackQueryHandler(
                callback=handle_location, pattern=rf"^{BTN_LABEL_SPB}"
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_location_text_input_instead_of_choosing_button,
            ),
        ],
        ###########################################################################
        #
        # pattern=rf"^{BTN_LABEL_BED_IN_ROOM}|{BTN_LABEL_ROOM_IN_APPARTMENT}"
        # переделать
        ##########################################################################
        states.ROOM_TYPE: [
            CallbackQueryHandler(
                callback=handle_room_type,
                pattern=rf"^{BTN_LABEL_BED_IN_ROOM}",
            ),
            CallbackQueryHandler(
                callback=handle_room_type,
                pattern=rf"^{BTN_LABEL_ROOM_IN_APPARTMENT}",
            ),
            CallbackQueryHandler(
                callback=handle_room_type,
                pattern=rf"^{BTN_LABEL_ROOM_IN_HOUSE}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_room_type_text_input_instead_of_choosing_button,
            ),
        ],
        states.ABOUT_ROOM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, handle_about_coliving
            ),
        ],
        states.PRICE: [
            MessageHandler(
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
                callback=handle_confirm_or_edit_reply_confirm,
                pattern=rf"^{BTN_LABEL_CONFIRM}",
            ),
            CallbackQueryHandler(
                callback=handle_confirm_or_edit_reply_edit_profile,
                pattern=rf"^{BTN_LABEL_EDIT_PROFILE_KEYBOARD}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_confirm_or_edit_profile_text_instead_of_button,
            ),
        ],
        states.EDIT: [
            CallbackQueryHandler(
                callback=handle_what_to_edit_fill_again,
                pattern=rf"^{BTN_LABEL_FILL_AGAIN}",
            ),
            CallbackQueryHandler(
                callback=handle_what_to_edit_room_type,
                pattern=rf"^{BTN_LABEL_EDIT_ROOM_TYPE}",
            ),
            CallbackQueryHandler(
                callback=handle_what_to_edit_location,
                pattern=rf"^{BTN_LABEL_EDIT_LOCATION}",
            ),
            CallbackQueryHandler(
                callback=handle_what_to_edit_about_room,
                pattern=rf"^{BTN_LABEL_EDIT_ABOUT_ROOM}",
            ),
            CallbackQueryHandler(
                callback=handle_what_to_edit_price,
                pattern=rf"^{BTN_LABEL_EDIT_PRICE}",
            ),
            CallbackQueryHandler(
                callback=handle_what_to_edit_photo_room,
                pattern=rf"^{BTN_LABEL_EDIT_PHOTO}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_what_to_edit_text_instead_of_button,
            ),
        ],
        states.IS_VISIBLE: [
            CallbackQueryHandler(
                callback=handle_is_visible_coliving_profile_yes,
                pattern=r"^show",
            ),
            CallbackQueryHandler(
                callback=handle_is_visible_coliving_profile_no,
                pattern=r"^hide",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_is_visible_coliving_profile_text_instead_of_button,
            ),
        ],
        states.EDIT_LOCATION: [
            CallbackQueryHandler(
                callback=handle_edit_location, pattern=rf"^{BTN_LABEL_MOSCOW}"
            ),
            CallbackQueryHandler(
                callback=handle_edit_location, pattern=rf"^{BTN_LABEL_SPB}"
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_location_text_input_instead_of_choosing_button,
            ),
        ],
        states.EDIT_ROOM_TYPE: [
            CallbackQueryHandler(
                callback=handle_edit_select_room_type,
                pattern=rf"^{BTN_LABEL_BED_IN_ROOM}",
            ),
            CallbackQueryHandler(
                callback=handle_edit_select_room_type,
                pattern=rf"^{BTN_LABEL_ROOM_IN_HOUSE}",
            ),
            CallbackQueryHandler(
                callback=handle_edit_select_room_type,
                pattern=rf"^{BTN_LABEL_ROOM_IN_HOUSE}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_room_type_text_input_instead_of_choosing_button,
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
                callback=handle_edit_profile_confirmation_confirm,
                pattern=rf"^{BTN_LABEL_CONFIRM}",
            ),
            CallbackQueryHandler(
                callback=handle_edit_profile_confirmation_cancel,
                pattern=rf"^{BTN_LABEL_CANCEL_EDIT}",
            ),
            CallbackQueryHandler(
                callback=handle_edit_profile_confirmation_continue_edit,
                pattern=rf"^{BTN_LABEL_EDIT_CONTINUE}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_edit_profile_confirmation_text_instead_of_button,
            ),
        ],
        states.COLIVING: [
            CallbackQueryHandler(
                callback=handle_coliving_edit,
                pattern=rf"^{BTN_LABEL_EDIT_PROFILE_KEYBOARD}",
            ),
            CallbackQueryHandler(
                callback=handle_coliving_show, pattern=r"^show"
            ),
            CallbackQueryHandler(
                callback=handle_coliving_hide, pattern=r"^hide"
            ),
            CallbackQueryHandler(
                callback=handle_coliving_roommates,
                pattern=r"^roommates_profiles",
            ),
            CallbackQueryHandler(
                callback=handle_coliving_views, pattern=r"^views"
            ),
            CallbackQueryHandler(
                callback=handle_coliving_transfer_to, pattern=r"^transfer_to"
            ),
            CallbackQueryHandler(
                callback=handle_coliving_go_to_menu, pattern=r"^go_to_menu"
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_coliving_text_instead_of_button,
            ),
        ],
    },
    fallbacks=[],
)
