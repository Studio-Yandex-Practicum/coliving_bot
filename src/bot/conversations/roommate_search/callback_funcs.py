from dataclasses import asdict

from telegram import (
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
    ReplyKeyboardRemove,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import conversations.roommate_search.keyboards as keyboards
import conversations.roommate_search.states as states
import conversations.roommate_search.templates as templates
from internal_requests import api_service
from internal_requests.entities import SearchSettings, UserProfile


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало ветви общения по поиску соседа.
    Проверяет, был ли настроен поиск ранее и, в зависимости от проверки,
    переводит либо в состояние подтверждения настроек, либо в настройку поиска.
    """
    search_settings = context.user_data.get("search_settings")
    if search_settings:
        await _message_edit(
            message=update.effective_message,
            text=templates.format_search_settings_message(search_settings),
        )
        await update.effective_message.reply_text(
            text=templates.ASK_SEARCH_SETTINGS,
            reply_markup=keyboards.SEARCH_SETTINGS_KEYBOARD,
        )
        return states.SEARCH_SETTINGS
    state = await edit_settings(update, context)
    return state


async def ok_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Вызывается при подтверждении настроек поиска.
    Получает список подходящих анкет и переводит в состояние оценки профиля соседа.
    """
    search_settings = context.user_data.get("search_settings")
    user_profiles = await api_service.get_filtered_user_profiles(
        filters=search_settings, viewer=update.effective_chat.id
    )
    state = await _get_next_user_profile(update, context, user_profiles)
    return state


async def edit_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Запускает процесс настройки поиска при запросе на изменение.
    Переводит в состояние выбора локации.
    """
    await _clear_roommate_search_context(context)
    await _message_edit(
        message=update.effective_message,
        text=templates.ASK_LOCATION,
        keyboard=context.bot_data["location_keyboard"],
    )
    return states.LOCATION


async def set_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает локацию в настройках поиска.
    Переводит в состояние выбора пола соседа.
    """
    location = update.callback_query.data.split(":")[1]
    context.user_data["search_settings"] = SearchSettings(location=location)
    await _message_edit(
        message=update.effective_message,
        text=templates.ASK_SEX,
        keyboard=keyboards.SEX_KEYBOARD,
    )
    return states.SEX


async def set_sex(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает пол соседа в настройках поиска.
    Переводит в состояние выбора возраста.
    """
    context.user_data["search_settings"].sex = update.callback_query.data
    await _message_edit(
        message=update.effective_message,
        text=templates.ASK_AGE,
        keyboard=keyboards.AGE_KEYBOARD,
    )
    return states.AGE


async def set_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает возраст соседа в настройках поиска.
    Переводит в состояние подтверждения настроек поиска.
    """
    callback_data = update.callback_query.data
    try:
        (
            context.user_data["search_settings"].age_min,
            context.user_data["search_settings"].age_max,
        ) = callback_data.split("-")
    except ValueError as exception:
        if callback_data.startswith(">"):
            context.user_data["search_settings"].age_min = callback_data.replace(
                ">", ""
            )
        else:
            raise exception
    search_settings = context.user_data.get("search_settings")
    await _message_edit(
        message=update.effective_message,
        text=templates.format_search_settings_message(search_settings),
    )
    await update.effective_message.reply_text(
        text=templates.ASK_SEARCH_SETTINGS,
        reply_markup=keyboards.SEARCH_SETTINGS_KEYBOARD,
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
    await api_service.send_match_request(
        sender=update.effective_chat.id, receiver=current_profile["user"]
    )

    await context.bot.send_message(
        chat_id=current_profile["user"],
        text=templates.LIKE_NOTIFICATION,
        reply_markup=keyboards.ANSWER_LIKE,
        parse_mode=ParseMode.HTML,
    )

    await update.effective_message.reply_text(
        text=templates.ASK_NEXT_PROFILE,
        reply_markup=keyboards.NEXT_PROFILE,
        parse_mode=ParseMode.HTML,
    )
    return states.NEXT_PROFILE


async def end_of_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Заканчивает ветку общения по поиску соседа.
    """
    if update.callback_query:
        await update.effective_message.delete()
    await update.effective_chat.send_message(
        text=templates.END_OF_SEARCH,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )
    await _clear_roommate_search_context(context)
    return ConversationHandler.END


async def _get_next_user_profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_profiles: list[UserProfile],
) -> int:
    """
    Функция для получения и вывода для оценки пользователю анкеты из списка анкет.
    Если анкеты заканчиваются - перевод в соответствующие состояние.
    """
    if update.callback_query:
        await update.effective_message.delete()
    if user_profiles:
        if context.user_data.get("current_profile") is None:
            await update.effective_chat.send_message(
                text=templates.SEARCH_INTRO,
                reply_markup=keyboards.PROFILE_KEYBOARD,
                parse_mode=ParseMode.HTML,
            )
        profile = asdict(user_profiles.pop())
        context.user_data["current_profile"] = profile
        context.user_data["user_profiles"] = user_profiles
        images = profile.pop("images")
        message_text = templates.PROFILE_DATA.format(**profile)
        if images:
            media_group = [InputMediaPhoto(file_id) for file_id in images]
            await update.effective_chat.send_media_group(
                media=media_group, caption=message_text, parse_mode=ParseMode.HTML
            )
        else:
            await update.effective_chat.send_message(
                text=message_text,
                reply_markup=keyboards.PROFILE_KEYBOARD,
                parse_mode=ParseMode.HTML,
            )
        return states.PROFILE

    await update.effective_message.reply_text(
        text=templates.NO_MATCHES,
        reply_markup=keyboards.NO_MATCHES_KEYBOARD,
        parse_mode=ParseMode.HTML,
    )
    return states.NO_MATCHES


async def _message_edit(
    message: Message,
    text: str,
    keyboard: InlineKeyboardMarkup | None = None,
) -> None:
    """
    Функция для изменения текста и клавиатуры сообщения с ParseMode.HTML.
    """
    await message.edit_text(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def _clear_roommate_search_context(context):
    context.user_data.pop("user_profiles", None)
    context.user_data.pop("current_profile", None)
