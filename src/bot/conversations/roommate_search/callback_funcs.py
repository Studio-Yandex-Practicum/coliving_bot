from dataclasses import asdict

from telegram import Update, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ContextTypes, ConversationHandler
)
from telegram._utils.defaultvalue import DEFAULT_NONE
from telegram._utils.types import ODVInput

import conversations.roommate_search.keyboards as keyboards
import conversations.roommate_search.templates as templates
from internal_requests import mock as api_service
from internal_requests.entities import UserProfile
from .constants import AGE_GROUP
from .states import RoommateSearchStates as states


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало ветви общения по поиску соседа.
    Проверяет, был ли настроен поиск ранее и, в зависимости от проверки,
    переводит либо в состояние подтверждения настроек, либо в настройку поиска.
    """
    search_settings = context.user_data.get("search_settings")
    if search_settings:
        await update.effective_message.reply_text(
            text=templates.CURRENT_SEARCH_SETTINGS.format(**search_settings),
            parse_mode=ParseMode.HTML
        )
        await update.effective_message.reply_text(
            text=templates.ASK_SEARCH_SETTINGS,
            reply_markup=keyboards.SEARCH_SETTINGS_KEYBOARD
        )
        return states.SEARCH_SETTINGS
    await update.effective_message.reply_text(
            text=templates.ASK_LOCATION,
            reply_markup=keyboards.LOCATION_KEYBOARD
        )
    return states.LOCATION


async def ok_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Вызывается при подтверждении настроек поиска.
    Получает список подходящих анкет и переводит в состояние оценки профиля соседа.
    """
    search_settings = context.user_data.get("search_settings")
    age_group = search_settings.get("age")
    user_profiles = await api_service.get_filtered_users(
        searcher_id=update.effective_chat.id,
        location=search_settings.get("location"),
        sex=search_settings.get("sex"),
        age_min=AGE_GROUP[age_group][0],
        age_max=AGE_GROUP[age_group][1],
    )
    state = await _get_next_user_profile(update, context, user_profiles)
    return state


async def edit_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Запускает процесс настройки поиска при запросе на изменение.
    Переводит в состояние выбора локации.
    """
    await _message_edit(
        update=update,
        text=templates.ASK_LOCATION,
        keyboard=keyboards.LOCATION_KEYBOARD
    )
    return states.LOCATION


async def set_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает локацию в настройках поиска.
    Переводит в состояние выбора пола соседа.
    """
    context.user_data["search_settings"] = dict()
    context.user_data["search_settings"]["location"] = update.callback_query.data
    await _message_edit(
        update=update,
        text=templates.ASK_SEX,
        keyboard=keyboards.SEX_KEYBOARD
    )
    return states.SEX


async def set_sex(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает пол соседа в настройках поиска.
    Переводит в состояние выбора возраста.
    """
    context.user_data["search_settings"]["sex"] = update.callback_query.data
    await _message_edit(
        update=update,
        text=templates.ASK_AGE,
        keyboard=keyboards.AGE_KEYBOARD
    )
    return states.AGE


async def set_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает возраст соседа в настройках поиска.
    Переводит в состояние подтверждения настроек поиска.
    """
    context.user_data["search_settings"]["age"] = update.callback_query.data
    search_settings = context.user_data.get("search_settings")
    await _message_edit(
        update=update,
        text=templates.CURRENT_SEARCH_SETTINGS.format(**search_settings),
        parse_mode=ParseMode.HTML
    )
    await update.effective_message.reply_text(
            text=templates.ASK_SEARCH_SETTINGS,
            reply_markup=keyboards.SEARCH_SETTINGS_KEYBOARD
        )
    return states.SEARCH_SETTINGS


async def next_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает переход на следующий профиль соседа.
    Удаляет анкету из выборки и переводит в состояние оценки анкеты,
    либо завершает поиск, если анкет больше нет.
    """
    user_profiles = context.user_data["user_profiles"]
    state = await _get_next_user_profile(update, context, user_profiles)
    return state


async def profile_like(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает ЛАЙК на профиль соседа.
    Посылает POST запрос в API на добавление MatchRequest,
    отправляет уведомление другому пользователю о лайке
    и переводит в состояние продолжения поиска.
    """
    current_profile = context.user_data.get("current_profile")
    roommate_id = current_profile.get("telegram_id")
    status = await api_service.post_match_request(
        sender_id=update.effective_user.id,
        reciever_id=roommate_id
    )

    # DEV/DEBUG - Обработка несуществующего roommate_id
    try:
        await context.bot.send_message(
            chat_id=roommate_id,
            text=templates.LIKE_NOTIFICATION
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text=templates.LIKE_NOTIFICATION
        )

    await _message_delete_and_reply(
        update=update,
        text=templates.ASK_NEXT_PROFILE,
        keyboard=keyboards.NEXT_PROFILE
    )
    return states.NEXT_PROFILE


async def end_of_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Заканчивает ветку общения по поиску соседа.
    """
    await _message_delete_and_reply(
        update=update,
        text=templates.END_OF_SEARCH
    )
    return ConversationHandler.END


async def _get_next_user_profile(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        user_profiles: list[UserProfile]
        ) -> int:
    """
    Функция для получения и вывода для оценки пользователю анкеты из списка анкет.
    Если анкеты заканчиваются - перевод в соответствующие состояние.
    """
    if user_profiles:
        profile = asdict(user_profiles.pop())
        context.user_data["current_profile"] = profile
        context.user_data["user_profiles"] = user_profiles
        await update.callback_query.message.delete()
        await update.callback_query.message.reply_photo(
            # photo=profile["images"],
            photo=open(profile["images"], 'rb'),  # DEV
            caption=templates.PROFILE_DATA.format(**profile),
            parse_mode=ParseMode.HTML,
            reply_markup=keyboards.PROFILE_KEYBOARD
        )
        return states.PROFILE

    await _message_delete_and_reply(
        update=update,
        text=templates.NO_MATCHES,
        keyboard=keyboards.NO_MATCHES_KEYBOARD
    )
    return states.NO_MATCHES


async def _message_edit(
        update: Update,
        text: str,
        keyboard: InlineKeyboardMarkup | None = None,
        parse_mode: ODVInput[str] = DEFAULT_NONE,
        ) -> None:
    await update.callback_query.message.edit_reply_markup()
    await update.callback_query.message.edit_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=parse_mode
        )


async def _message_delete_and_reply(
        update: Update,
        text: str,
        keyboard: InlineKeyboardMarkup | None = None
        ) -> None:
    await update.callback_query.message.delete()
    await update.effective_message.reply_text(
            text=text,
            reply_markup=keyboard
        )
