from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import conversations.complain.buttons as buttons
import conversations.complain.callback_funcs as callbacks
from conversations.common_functions import common_funcs
from conversations.complain import states
from conversations.menu.constants import CANCEL_COMMAND, MENU_COMMAND
from general.validators import handle_text_input_instead_of_choosing_button
from internal_requests.entities import Categories

AGREE_REGEX_PATTERN = rf"^(?P<{'reported_user_id'}>\d+)" r":{}$"


complain_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=common_funcs.add_response_prefix()(common_funcs.cancel),
            pattern=AGREE_REGEX_PATTERN.format(buttons.REPORT_NO_BUTTON),
        ),
        CallbackQueryHandler(
            callback=callbacks.category_choose,
            pattern=AGREE_REGEX_PATTERN.format(buttons.REPORT_YES_BUTTON),
        ),
    ],
    states={
        states.COMPLAIN_TEXT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callbacks.handle_complain_text,
            )
        ],
        states.CATEGORY: [
            CallbackQueryHandler(
                callback=callbacks.handle_category,
                pattern=(
                    rf"^({Categories.CATEGORY_SPAM.value}"
                    f"|{Categories.CATEGORY_BAD_LANG.value}"
                    f"|{Categories.CATEGORY_CHEATER.value}"
                    f"|{Categories.CATEGORY_INCORRECT_DATA.value}"
                    f"|{Categories.CATEGORY_PROHIB_ACTIV.value}"
                    f"|{Categories.CATEGORY_OTHER.value})$"
                ),
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.SCREENSHOT: [
            CallbackQueryHandler(
                callback=callbacks.attach_screenshot,
                pattern=rf"^{buttons.SCREEN_YES_BUTTON}$",
            ),
            CallbackQueryHandler(
                callback=callbacks.final_report,
                pattern=rf"^{buttons.SCREEN_NO_BUTTON}$",
            ),
            MessageHandler(filters.PHOTO, callbacks.handle_screenshot),
        ],
    },
    fallbacks=[
        CommandHandler(
            command=CANCEL_COMMAND,
            callback=common_funcs.add_response_prefix()(common_funcs.cancel),
        ),
        CommandHandler(
            command=MENU_COMMAND,
            callback=common_funcs.return_to_menu_via_menu_command,
        ),
    ],
)
