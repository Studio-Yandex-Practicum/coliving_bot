from telegram.ext import (
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import conversations.profile.buttons as buttons
import conversations.profile.callback_funcs as callback_funcs
import conversations.profile.templates as templates
from conversations.common_functions import common_buttons, common_funcs
from conversations.menu.buttons import MY_PROFILE_BUTTON
from conversations.profile.states import States
from general.validators import (
    handle_text_input_instead_of_choosing_button,
    handle_text_input_instead_of_send_photo,
)

profile_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            pattern=rf"^{MY_PROFILE_BUTTON}$", callback=callback_funcs.start
        ),
    ],
    states={
        States.PROFILE: [
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_profile_is_visible_in_search,
                pattern=(
                    rf"^({common_buttons.SHOW_SEARCH_BUTTON}"
                    rf"|{common_buttons.HIDE_SEARCH_BUTTON})$"
                ),
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_edit_profile,
                pattern=rf"^{buttons.EDIT_FORM_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_return_to_menu_response,
                pattern=rf"^{common_buttons.RETURN_TO_MENU_BTN_LABEL}",
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
                pattern=common_buttons.LOCATION_CALLBACK_PATTERN,
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
            CallbackQueryHandler(
                pattern=rf"^{buttons.SAVE_PHOTO_BUTTON}",
                callback=callback_funcs.send_received_photos,
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
                    rf"^({common_buttons.SHOW_SEARCH_BUTTON}"
                    rf"|{common_buttons.HIDE_SEARCH_BUTTON})$"
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
                callback=callback_funcs.handle_return_to_profile_response,
                pattern=rf"^{common_buttons.RETURN_BTN_LABEL}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_edit_name,
                pattern=rf"^{buttons.EDIT_NAME_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_edit_sex,
                pattern=rf"^{buttons.EDIT_SEX_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_edit_age,
                pattern=rf"^{buttons.EDIT_AGE_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_edit_location,
                pattern=rf"^{buttons.EDIT_LOCATION_BUTTON}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.send_question_to_edit_about_myself,
                pattern=rf"^{buttons.EDIT_ABOUT_BUTTON}",
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
            CallbackQueryHandler(
                callback_funcs.handle_edit_sex,
                rf"^({buttons.MALE_BUTTON}|{buttons.FEMALE_BUTTON})$",
            )
        ],
        States.EDIT_AGE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, callback_funcs.handle_edit_age
            )
        ],
        States.EDIT_LOCATION: [
            CallbackQueryHandler(
                callback_funcs.handle_edit_location,
                common_buttons.LOCATION_CALLBACK_PATTERN,
            )
        ],
        States.EDIT_ABOUT_YOURSELF: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, callback_funcs.handle_edit_about
            )
        ],
        States.EDIT_PHOTO: [
            MessageHandler(filters.PHOTO, callback_funcs.handle_edit_photo),
            CallbackQueryHandler(
                pattern=rf"^{buttons.SAVE_EDITED_PHOTO_BUTTON}",
                callback=callback_funcs.send_edited_photos,
            ),
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
    fallbacks=[
        CallbackQueryHandler(
            callback=common_funcs.cancel,
            pattern=rf"^{common_buttons.CANCEL_BUTTON}",
        ),
    ],
)
