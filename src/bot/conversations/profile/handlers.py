from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import conversations.profile.buttons as buttons
import conversations.profile.callback_funcs as callback_funcs
import conversations.profile.templates as templates
from conversations.menu.buttons import MY_PROFILE_BUTTON
from conversations.profile.states import States
from general.validators import (
    handle_text_input_instead_of_choosing_button,
    handle_text_input_instead_of_send_photo,
)

profile_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CommandHandler(command="profile", callback=callback_funcs.start),
        CallbackQueryHandler(
            pattern=rf"^{MY_PROFILE_BUTTON}$", callback=callback_funcs.start
        ),
    ],
    states={
        States.PROFILE: [
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_profile_is_visible_in_search,
                pattern=rf"^{buttons.SHOW_SEARCH_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_profile_is_invisible_in_search,
                pattern=rf"^{buttons.HIDE_SEARCH_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_edit_profile,
                pattern=rf"^{buttons.EDIT_FORM_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_back_in_menu,
                pattern=rf"^{buttons.BACK_BUTTON}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.AGE: [
            MessageHandler(
                filters.Regex(rf"{templates.AGE_PATTERN}") & ~filters.COMMAND,
                callback_funcs.handle_age,
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, callback_funcs.handle_age),
        ],
        States.SEX: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_sex,
                pattern=rf"^({buttons.MALE_BUTTON}|{buttons.FEMALE_BUTTON})$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, callback_funcs.handle_name),
        ],
        States.LOCATION: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_location,
                pattern=rf"^({buttons.MSK_BUTTON}|{buttons.SPB_BUTTON})$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.ABOUT_YOURSELF: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, callback_funcs.handle_about)
        ],
        States.PHOTO: [
            MessageHandler(
                filters.PHOTO & ~filters.COMMAND, callback_funcs.handle_photo
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_send_photo,
            ),
        ],
        States.CONFIRMATION: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_profile,
                pattern=rf"^({buttons.YES_BUTTON}|{buttons.EDIT_FORM_BUTTON})$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.VISIBLE: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_visible,
                pattern=(
                    rf"^({buttons.YES_TO_DO_BUTTON}|{buttons.NOT_LOOK_YET_BUTTON})$"
                ),
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.EDIT: [
            CallbackQueryHandler(
                callback=callback_funcs.start_filling_again,
                pattern=rf"^{buttons.FILL_AGAIN_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_back_to_profile,
                pattern=rf"^{buttons.BACK_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_edit_name,
                pattern=rf"^{buttons.NEW_NAME_NEW_BEGINNING_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_edit_sex,
                pattern=rf"^{buttons.SEX_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_edit_age,
                pattern=rf"^{buttons.AGE_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_edit_location,
                pattern=rf"^{buttons.LOCATION_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_edit_about_myself,
                pattern=rf"^{buttons.ABOUT_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_edit_photo,
                pattern=rf"^{buttons.NEW_PHOTO_BUTTON}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        States.EDIT_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, callback_funcs.handle_edit_name
            )
        ],
        States.EDIT_SEX: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, callback_funcs.handle_edit_sex
            )
        ],
        States.EDIT_AGE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, callback_funcs.handle_edit_age
            )
        ],
        States.EDIT_LOCATION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, callback_funcs.handle_edit_location
            )
        ],
        States.EDIT_ABOUT_YOURSELF: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, callback_funcs.handle_edit_about
            )
        ],
        States.EDIT_PHOTO: [
            MessageHandler(filters.PHOTO, callback_funcs.handle_edit_photo),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_send_photo,
            ),
        ],
        States.EDIT_CONFIRMATION: [
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_profile_is_correct,
                pattern=rf"^{buttons.YES_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_cancel_profile_edit,
                pattern=rf"^{buttons.EDIT_CANCEL_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_resume_profile_edit,
                pattern=rf"^{buttons.EDIT_RESUME_BUTTON}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
    },
    fallbacks=[],
)
