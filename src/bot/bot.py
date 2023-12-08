from telegram.ext import ApplicationBuilder, Application

from src.bot.utils.config import TOKEN


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(TOKEN).build()
    return application
