import datetime
from typing import Optional

from telegram.ext import (
    AIORateLimiter,
    Application,
    ApplicationBuilder,
    CommandHandler,
    Defaults,
)

from conversations.coliving.handlers import coliving_handler
from conversations.coliving.keyboards import create_keyboard_of_locations
from conversations.coliving_search.handlers import coliving_search_handler
from conversations.complain.handlers import complain_handler
from conversations.invitation.handlers import invitation_handler
from conversations.match_requests.coliving.handlers import coliving_like_handler
from conversations.match_requests.profile.handlers import profile_like_handler
from conversations.menu.callback_funcs import menu, start
from conversations.menu.constants import MENU_COMMAND, START_COMMAND
from conversations.menu.handlers import menu_handler
from conversations.menu.keyboards import get_main_menu_commands
from conversations.profile.handlers import profile_handler
from conversations.roommate_search.handlers import roommate_search_handler
from error_handler.callback_funcs import error_handler
from regular_tasks.likes import delete_old_likes
from regular_tasks.locations import update_location_keyboard
from regular_tasks.mailing import check_mailing_list
from regular_tasks.useful_info import update_useful_materials_for_relevance
from utils.configs import TOKEN


async def post_init(application: Application) -> None:
    """Создает кнопку меню и наполняет ее командами."""
    await application.bot.set_my_commands(get_main_menu_commands())
    application.bot_data["location_keyboard"] = await create_keyboard_of_locations()


def create_bot_app(defaults: Optional[Defaults] = None) -> Application:
    rate_limiter = AIORateLimiter(max_retries=1)
    application: Application = (
        ApplicationBuilder()
        .token(TOKEN)
        .rate_limiter(rate_limiter)
        .defaults(defaults)
        .post_init(post_init)
        .build()
    )
    application.add_handler(CommandHandler(START_COMMAND, start))
    application.add_handler(handler=coliving_handler)
    application.add_handler(handler=profile_handler)
    application.add_handler(handler=roommate_search_handler)
    application.add_handler(handler=coliving_search_handler)
    application.add_handler(handler=complain_handler)
    application.add_handler(handler=invitation_handler)
    application.add_handler(handler=profile_like_handler)
    application.add_handler(handler=coliving_like_handler)
    application.add_handler(handler=menu_handler)
    application.add_handler(CommandHandler(MENU_COMMAND, menu))
    application.add_error_handler(error_handler)

    _setup_job_queue(application)

    return application


def _setup_job_queue(application):
    job_queue = application.job_queue
    job_queue.run_daily(
        delete_old_likes,
        time=datetime.time(hour=1, minute=0, second=0),
    )

    job_queue.run_daily(
        update_location_keyboard,
        time=datetime.time(hour=1, minute=0, second=0),
    )

    job_queue.run_repeating(
        update_useful_materials_for_relevance,
        interval=datetime.timedelta(hours=1),
    )

    job_queue.run_repeating(
        check_mailing_list,
        interval=datetime.timedelta(hours=1),
        first=_seconds_until_next_hour(),
    )


def _seconds_until_next_hour() -> float:
    """Возвращает кол-во секунд до следующего часа."""
    current_time = datetime.datetime.now()
    next_hour = current_time.replace(
        hour=(current_time.hour + 1) % 24, minute=0, second=0, microsecond=0
    )
    if next_hour.hour == 0:
        next_hour += datetime.timedelta(days=1)
    delay = (next_hour - current_time).total_seconds()
    return delay
