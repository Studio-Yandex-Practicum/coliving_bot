from telegram.ext import Application, ApplicationBuilder

from conversations.menu.handlers import start_and_menu_handler
from conversations.menu.keyboards import get_main_menu_commands
from conversations.profile.handlers import profile_handler
from utils.configs import TOKEN


async def post_init(application: Application) -> None:
    """Создает кнопку меню и наполняет ее командами."""
    await application.bot.set_my_commands(get_main_menu_commands())


def create_bot_app() -> Application:
    application: Application = (
        ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    )
    application.add_handler(handler=start_and_menu_handler)
    application.add_handler(handler=profile_handler)
    return application
