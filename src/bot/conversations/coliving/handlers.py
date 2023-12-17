from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, filters, MessageHandler)

from .callback_funcs import (about_coliving, photo, price,
                             select_bed_in_room_type,
                             select_moscow_location,
                             select_room_in_apartment_type,
                             select_room_in_house_type,
                             select_spb_location,
                             start)
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
        ],
        states.ABOUT_ROOM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, about_coliving
            ),
        ],
        states.PRICE: [
            MessageHandler(
                #filters.Regex(r'^([0-9]{4})$') & ~filters.COMMAND, price
                filters.Regex(r'^(\d*)$') & ~filters.COMMAND, price
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, price),
        ],
        states.PHOTO_ROOM: [
            MessageHandler(
                filters.PHOTO, photo)
        ],
    },
    fallbacks=[],
)


# entry_point_to_coliving_handler = CommandHandler(
#     "coliving", coliving
# )
