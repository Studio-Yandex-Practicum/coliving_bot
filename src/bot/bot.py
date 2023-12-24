from telegram.ext import Application, ApplicationBuilder

from error_handler.callback_funcs import error_handler
from utils.configs import TOKEN


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(TOKEN).build()
    application.add_error_handler(error_handler)
    return application
