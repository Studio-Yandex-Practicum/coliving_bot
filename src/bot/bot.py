from telegram.ext import Application, ApplicationBuilder
from utils.config import TOKEN


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(TOKEN).build()
    return application
