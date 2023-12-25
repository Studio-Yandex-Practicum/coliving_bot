from telegram.ext import Application, ApplicationBuilder, CommandHandler

from conversations.start.callback_funcs import start
from utils.configs import TOKEN


def create_bot_app() -> Application:
    application: Application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    return application
