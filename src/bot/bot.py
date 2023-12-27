from telegram.ext import Application, ApplicationBuilder

from conversations.coliving.handlers import coliving_handler
from utils.configs import TOKEN


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(handler=coliving_handler)
    return application
