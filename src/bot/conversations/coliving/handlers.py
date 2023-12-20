from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, filters, MessageHandler)

from .callback_funcs import (about_coliving, photo,
                             confirm_or_edit_profile,
                             edit_about_coliving,
                             edit_photo_room,
                             edit_price,
                             edit_profile_confirmation,
                             edit_select_room_type,
                             is_visible_coliving_profile,
                             location_not_text,
                             price,
                             room_type_not_text,
                             select_bed_in_room_type,
                             select_moscow_location,
                             select_room_in_apartment_type,
                             select_room_in_house_type,
                             select_spb_location,
                             show_coliving_profile,
                             start,
                             what_to_edit)
from .states import ColivingStates as states
from .templates import COLIVING, LOCATION_MOSCOW_BTN_TEXT, LOCATION_SPB_BTN_TEXT


acquaintance_handler: ConversationHandler = ConversationHandler(
    entry_points=[CommandHandler(COLIVING, start)],
    states={
        states.LOCATION: [
            CallbackQueryHandler(
                callback=select_moscow_location,
                pattern=r"^moscow_city"
            ),
            CallbackQueryHandler(
                callback=select_spb_location,
                pattern=r"^spb_city"
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                location_not_text,
            ),
        ],
        states.ROOM_TYPE: [
            CallbackQueryHandler(
                callback=select_bed_in_room_type,
                pattern=r"^bed_in_room"
            ),
            CallbackQueryHandler(
                callback=select_room_in_apartment_type,
                pattern=r"^room_in_apartment"
            ),
            CallbackQueryHandler(
                callback=select_room_in_house_type,
                pattern=r"^room_in_house"
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                room_type_not_text,
            ),
        ],
        states.ABOUT_ROOM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                about_coliving
            ),
        ],
        states.PRICE: [
            MessageHandler(
                #filters.Regex(r'^([0-9]{4})$') & ~filters.COMMAND, price
                filters.Regex(r'^(\d*)$') & ~filters.COMMAND,
                price
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                price
            ),
        ],
        states.PHOTO_ROOM: [
            MessageHandler(
                filters.PHOTO & ~filters.COMMAND,
                photo
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                photo
            ),
        ],
        states.CONFIRMATION: [
            CallbackQueryHandler(
                callback=confirm_or_edit_profile,
                pattern=r'^confirm'
            ),
            CallbackQueryHandler(
                callback=confirm_or_edit_profile,
                pattern=r'^edit_profile'
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                show_coliving_profile
            ),
        ],
        states.EDIT: [
            CallbackQueryHandler(
                callback=what_to_edit,
                pattern=r'^edit_fill_again'
            ),
            CallbackQueryHandler(
                callback=what_to_edit,
                pattern=r'^edit_room_type'
            ),
            CallbackQueryHandler(
                callback=what_to_edit,
                pattern=r'^edit_description'
            ),
            CallbackQueryHandler(
                callback=what_to_edit,
                pattern=r'^edit_price'
            ),
            CallbackQueryHandler(
                callback=what_to_edit,
                pattern=r'^edit_send_photo'
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                what_to_edit
            ),
        ],
        states.IS_VISIBLE: [
            CallbackQueryHandler(
                callback=is_visible_coliving_profile,
                pattern=r'^show'
            ),
            CallbackQueryHandler(
                callback=is_visible_coliving_profile,
                pattern=r'^hide'
            ),
        ],
        states.EDIT_ROOM_TYPE: [
            CallbackQueryHandler(
                callback=edit_select_room_type,
                pattern=r'^bed_in_room'
            ),
            CallbackQueryHandler(
                callback=edit_select_room_type,
                pattern=r'^room_in_apartment'
            ),
            CallbackQueryHandler(
                callback=edit_select_room_type,
                pattern=r'^room_in_house'
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                room_type_not_text,
            ),
        ],
        states.EDIT_ABOUT_ROOM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                edit_about_coliving,
            ),
        ],
        states.EDIT_PRICE: [
            MessageHandler(
                #filters.Regex(r'^([0-9]{4})$') & ~filters.COMMAND, price
                filters.Regex(r'^(\d*)$') & ~filters.COMMAND,
                edit_price,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                edit_price,
            ),
        ],
        states.EDIT_PHOTO_ROOM: [
            MessageHandler(
                filters.PHOTO & ~filters.COMMAND,
                edit_photo_room,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                edit_photo_room,
            ),
        ],
        states.EDIT_CONFIRMATION: [
            CallbackQueryHandler(
                callback=edit_profile_confirmation,
                pattern=r'^confirm'
            ),
            CallbackQueryHandler(
                callback=edit_profile_confirmation,
                pattern=r'^edit_profile'
            ),
            CallbackQueryHandler(
                callback=edit_profile_confirmation,
                pattern=r'^cancel'
            ),
            CallbackQueryHandler(
                callback=edit_profile_confirmation,
                pattern=r'^continue_editing'
            ),
            # MessageHandler(filters.TEXT & ~filters.COMMAND, show_coliving_profile),
        ],

    },
    fallbacks=[],
)


# entry_point_to_coliving_handler = CommandHandler(
#     "coliving", coliving
# )
