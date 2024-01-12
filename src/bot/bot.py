from telegram.ext import Application, ApplicationBuilder, CommandHandler

from conversations.coliving.handlers import coliving_handler
from conversations.menu.callback_funcs import menu, start
from conversations.menu.keyboards import get_main_menu_commands
from conversations.profile.handlers import profile_handler
from error_handler.callback_funcs import error_handler
from utils.configs import TOKEN


async def post_init(application: Application) -> None:
    """Создает кнопку меню и наполняет ее командами."""
    await application.bot.set_my_commands(get_main_menu_commands())


def create_bot_app() -> Application:
    application: Application = (
        ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    )
    application.add_handler(handler=coliving_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(handler=profile_handler)
    application.add_error_handler(error_handler)
    return application
