from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from general.validators import (
    handle_text_input_instead_of_choosing_button,
    handle_text_input_instead_of_send_photo,
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
    handle_edit_about,
    handle_edit_photo,
    handle_location,
    handle_name,
    handle_photo,
    handle_profile,
    handle_sex,
    handle_visible,
    send_question_to_back_in_menu,
    send_question_to_cancel_profile_edit,
    send_question_to_edit_about_myself,
    send_question_to_edit_photo,
    send_question_to_edit_profile,
    send_question_to_profile_is_correct,
    send_question_to_profile_is_invisible_in_search,
    send_question_to_profile_is_visible_in_search,
    send_question_to_resume_profile_edit,
    start,
    start_filling_again,
)
from .states import States
from .templates import AGE_PATTERN

profile_handler: ConversationHandler = ConversationHandler(
    entry_points=[CommandHandler(command="profile", callback=start)],
    states={
        States.PROFILE: [
            CallbackQueryHandler(
                callback=send_question_to_profile_is_visible_in_search,
                pattern=rf"^{SHOW_SEARCH_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=send_question_to_profile_is_invisible_in_search,
                pattern=rf"^{HIDE_SEARCH_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=send_question_to_edit_profile,
                pattern=rf"^{EDIT_FORM_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=send_question_to_back_in_menu,
                pattern=rf"^{BACK_BUTTON}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.AGE: [
            MessageHandler(
                filters.Regex(rf"{AGE_PATTERN}") & ~filters.COMMAND, handle_age
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_age),
        ],
        States.SEX: [
            CallbackQueryHandler(
                callback=handle_sex,
                pattern=rf"^({MALE_BUTTON}|{FEMALE_BUTTON})$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name),
        ],
        States.LOCATION: [
            CallbackQueryHandler(
                callback=handle_location,
                pattern=rf"^({MSK_BUTTON}|{SPB_BUTTON})$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.ABOUT_YOURSELF: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_about)
        ],
        States.PHOTO: [
            MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_photo),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_send_photo,
            ),
        ],
        States.CONFIRMATION: [
            CallbackQueryHandler(
                callback=handle_profile,
                pattern=rf"^({YES_BUTTON}|{EDIT_FORM_BUTTON})$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.VISIBLE: [
            CallbackQueryHandler(
                callback=handle_visible,
                pattern=rf"^({YES_TO_DO_BUTTON}|{NOT_LOOK_YET_BUTTON})$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.EDIT: [
            CallbackQueryHandler(
                callback=start_filling_again, pattern=rf"^{FILL_AGAIN_BUTTON}"
            ),
            CallbackQueryHandler(
                callback=send_question_to_edit_about_myself,
                pattern=rf"^{ABOUT_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=send_question_to_edit_photo,
                pattern=rf"^{NEW_PHOTO_BUTTON}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.EDIT_ABOUT_YOURSELF: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_about)
        ],
        States.EDIT_PHOTO: [
            MessageHandler(filters.PHOTO, handle_edit_photo),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_send_photo,
            ),
        ],
        States.EDIT_CONFIRMATION: [
            CallbackQueryHandler(
                callback=send_question_to_profile_is_correct,
                pattern=rf"^{YES_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=send_question_to_cancel_profile_edit,
                pattern=rf"^{EDIT_CANCEL_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=send_question_to_resume_profile_edit,
                pattern=rf"^{EDIT_RESUME_BUTTON}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
    },
    fallbacks=[],
)
