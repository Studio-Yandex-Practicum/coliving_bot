from telegram.ext import ApplicationBuilder, Application

from utils.config import TOKEN


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(TOKEN).build()
    return application
