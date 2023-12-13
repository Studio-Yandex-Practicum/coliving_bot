from telegram.ext import Application, ApplicationBuilder
from utils.configs import TOKEN
from utils.logger import configure_logging

configure_logging()


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(TOKEN).build()
    return application
