from telegram.ext import Application, ApplicationBuilder, CommandHandler

from conversations.coliving.handlers import coliving_handler
from conversations.profile.handler import profile_handler
from conversations.start.callback_funcs import start
from error_handler.callback_funcs import error_handler
from utils.configs import TOKEN


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(handler=coliving_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(handler=profile_handler)
    application.add_error_handler(error_handler)
    return application
