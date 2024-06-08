import datetime
from typing import Optional

from telegram.ext import Application, ApplicationBuilder, CommandHandler, Defaults

from conversations.coliving.handlers import coliving_handler
from conversations.coliving.keyboards import create_keyboard_of_locations
from conversations.coliving_search.handlers import coliving_search_handler
from conversations.invitation.handlers import invitation_handler
from conversations.match_requests.coliving.handlers import coliving_like_handler
from conversations.match_requests.profile.handlers import profile_like_handler
from conversations.menu.callback_funcs import menu, start
from conversations.menu.constants import MENU_COMMAND, START_COMMAND
from conversations.menu.keyboards import get_main_menu_commands
from conversations.profile.handlers import profile_handler
from conversations.roommate_search.callback_funcs import delete_old_likes
from conversations.roommate_search.handlers import roommate_search_handler
from error_handler.callback_funcs import error_handler
from utils.configs import TOKEN


async def post_init(application: Application) -> None:
    """Создает кнопку меню и наполняет ее командами."""
    await application.bot.set_my_commands(get_main_menu_commands())
    application.bot_data["location_keyboard"] = await create_keyboard_of_locations()


def create_bot_app(defaults: Optional[Defaults] = None) -> Application:
    application: Application = (
        ApplicationBuilder()
        .token(TOKEN)
        .defaults(defaults)
        .post_init(post_init)
        .build()
    )
    application.add_handler(CommandHandler(START_COMMAND, start))
    application.add_handler(handler=coliving_handler)
    application.add_handler(handler=profile_handler)
    application.add_handler(handler=roommate_search_handler)
    application.add_handler(handler=coliving_search_handler)
    application.add_handler(handler=invitation_handler)
    application.add_handler(handler=profile_like_handler)
    application.add_handler(handler=coliving_like_handler)
    application.add_handler(CommandHandler(MENU_COMMAND, menu))
    application.add_error_handler(error_handler)
    job_queue = application.job_queue
    job_queue.run_daily(
        delete_old_likes, time=datetime.time(hour=0, minute=0, second=0)
    )
    return application
