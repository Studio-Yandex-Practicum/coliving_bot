from telegram.ext import Application, ApplicationBuilder
from utils.config import TOKEN
from conversations.profile.handler import profile_handler


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(handler=profile_handler)
    return application
