from telegram.ext import CallbackQueryHandler, ConversationHandler

from conversations.menu import callback_funcs
from conversations.menu.buttons import USEFUL_BUTTON

menu_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback_funcs.useful_info, f"^{USEFUL_BUTTON}$")
    ],
    states={},
    fallbacks=[],
)
