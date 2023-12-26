from telegram.ext import Application, ApplicationBuilder

from conversations.roommate_search.handlers import roommate_search_handler
from utils.configs import TOKEN


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(handler=roommate_search_handler)
    return application
