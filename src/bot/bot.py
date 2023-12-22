from telegram.ext import Application, ApplicationBuilder

from conversations.profile.handler import profile_handler
from utils.configs import TOKEN


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(handler=profile_handler)
    return application
