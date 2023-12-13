from telegram.ext import Application, ApplicationBuilder
from utils.configs import TOKEN


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(TOKEN).build()
    return application
