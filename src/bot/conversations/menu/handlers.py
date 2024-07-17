from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler

from conversations.common_functions import common_funcs
from conversations.menu import callback_funcs
from conversations.menu.buttons import USEFUL_INFO_BUTTON
from conversations.menu.constants import CANCEL_COMMAND, MENU_COMMAND

menu_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback_funcs.useful_info_menu,
            USEFUL_INFO_BUTTON,
        ),
    ],
    states={},
    fallbacks=[
        CommandHandler(
            command=CANCEL_COMMAND,
            callback=common_funcs.cancel,
        ),
        CommandHandler(
            command=MENU_COMMAND,
            callback=common_funcs.return_to_menu_via_menu_command,
        ),
    ],
)
