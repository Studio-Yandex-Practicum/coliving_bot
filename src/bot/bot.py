from telegram.ext import Application, ApplicationBuilder

from conversations.coliving.handlers import acquaintance_handler
from utils.configs import TOKEN


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(TOKEN).build()

    # энтри поинт /coliving
    application.add_handler(handler=acquaintance_handler)

    return application
