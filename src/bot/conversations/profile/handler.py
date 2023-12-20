from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from .buttons import (
    ABOUT_BUTTON,
    BACK_BUTTON,
    EDIT_CANCEL_BUTTON,
    EDIT_FORM_BUTTON,
    EDIT_RESUME_BUTTON,
    FEMALE_BUTTON,
    FILL_AGAIN_BUTTON,
    HIDE_SEARCH_BUTTON,
    MALE_BUTTON,
    MSK_BUTTON,
    NEW_PHOTO_BUTTON,
    NOT_LOOK_YET_BUTTON,
    SHOW_SEARCH_BUTTON,
    SPB_BUTTON,
    YES_BUTTON,
    YES_TO_DO_BUTTON,
)
from .callback_funcs import (
    handle_about,
    handle_age,
    handle_edit,
    handle_edit_about,
    handle_edit_confirmation,
    handle_edit_photo,
    handle_fill_profile,
    handle_location,
    handle_name,
    handle_photo,
    handle_profile,
    handle_sex,
    handle_visible,
    start,
)
from .states import States

profile_handler: ConversationHandler = ConversationHandler(
    entry_points=[CommandHandler(command="profile", callback=start)],
    states={
        States.PROFILE: [
            CallbackQueryHandler(
                callback=handle_fill_profile, pattern=rf"^{SHOW_SEARCH_BUTTON}"
            ),
            CallbackQueryHandler(
                callback=handle_fill_profile, pattern=rf"^{HIDE_SEARCH_BUTTON}"
            ),
            CallbackQueryHandler(
                callback=handle_fill_profile, pattern=rf"^{EDIT_FORM_BUTTON}"
            ),
            CallbackQueryHandler(
                callback=handle_fill_profile, pattern=rf"^{BACK_BUTTON}"
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, handle_fill_profile
            ),
        ],
        States.AGE: [
            MessageHandler(
                filters.Regex(r"^([0-9]{3})$") & ~filters.COMMAND, handle_age
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_age),
        ],
        States.SEX: [
            CallbackQueryHandler(
                callback=handle_sex, pattern=rf"^{MALE_BUTTON}"
            ),
            CallbackQueryHandler(
                callback=handle_sex, pattern=rf"^{FEMALE_BUTTON}"
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_sex),
        ],
        States.NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name),
        ],
        States.LOCATION: [
            CallbackQueryHandler(
                callback=handle_location, pattern=rf"^{MSK_BUTTON}"
            ),
            CallbackQueryHandler(
                callback=handle_location, pattern=rf"^{SPB_BUTTON}"
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_location),
        ],
        States.ABOUT_YOURSELF: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_about)
        ],
        States.PHOTO: [
            MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_photo),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_photo),
        ],
        States.CONFIRMATION: [
            CallbackQueryHandler(
                callback=handle_profile, pattern=rf"^{YES_BUTTON}"
            ),
            CallbackQueryHandler(
                callback=handle_profile, pattern=rf"^{EDIT_FORM_BUTTON}"
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_profile),
        ],
        States.VISIBLE: [
            CallbackQueryHandler(
                callback=handle_visible, pattern=rf"^{YES_TO_DO_BUTTON}"
            ),
            CallbackQueryHandler(
                callback=handle_visible, pattern=rf"^{NOT_LOOK_YET_BUTTON}"
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_visible),
        ],
        States.EDIT: [
            CallbackQueryHandler(
                callback=handle_edit, pattern=rf"^{FILL_AGAIN_BUTTON}"
            ),
            CallbackQueryHandler(
                callback=handle_edit, pattern=rf"^{ABOUT_BUTTON}"
            ),
            CallbackQueryHandler(
                callback=handle_edit, pattern=rf"^{NEW_PHOTO_BUTTON}"
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit),
        ],
        States.EDIT_ABOUT_YOURSELF: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_about)
        ],
        States.EDIT_PHOTO: [
            MessageHandler(filters.PHOTO, handle_edit_photo),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_photo),
        ],
        States.EDIT_CONFIRMATION: [
            CallbackQueryHandler(
                callback=handle_edit_confirmation, pattern=rf"^{YES_BUTTON}"
            ),
            CallbackQueryHandler(
                callback=handle_edit_confirmation,
                pattern=rf"^{EDIT_CANCEL_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=handle_edit_confirmation,
                pattern=rf"^{EDIT_RESUME_BUTTON}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, handle_edit_confirmation
            ),
        ],
    },
    fallbacks=[],
)
