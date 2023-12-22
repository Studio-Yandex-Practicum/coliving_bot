from telegram.ext import (
    CommandHandler,
    ConversationHandler,
)

from .callback_funcs import start, menu


start_and_menu_handler: ConversationHandler = ConversationHandler(
    entry_points=[
            CommandHandler(command="start", callback=start),
            CommandHandler(command="menu", callback=menu)
        ],
    states={},
    fallbacks=[],
)
