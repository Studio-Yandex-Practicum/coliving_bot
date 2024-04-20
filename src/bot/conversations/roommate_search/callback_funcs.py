from dataclasses import asdict

from telegram import (
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import ContextTypes, ConversationHandler

import conversations.match_requests.keyboards as match_keyboards
import conversations.match_requests.templates as match_templates
import conversations.roommate_search.keyboards as keyboards
import conversations.roommate_search.templates as templates
from conversations.common_functions.common_funcs import profile_required
from conversations.roommate_search.states import States
from internal_requests import api_service
from internal_requests.entities import ProfileSearchSettings, UserProfile


@profile_required
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
        return States.SEARCH_SETTINGS
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
    return States.LOCATION


async def set_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает локацию в настройках поиска.
    Переводит в состояние выбора пола соседа.
    """
    location = update.callback_query.data.split(":")[1]
    context.user_data["search_settings"] = ProfileSearchSettings(location=location)
    await _message_edit(
        message=update.effective_message,
        text=templates.ASK_SEX,
        keyboard=keyboards.SEX_KEYBOARD,
    )
    return States.SEX


async def set_sex(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает пол соседа в настройках поиска.
    Переводит в состояние выбора возраста.
    """
    sex = update.callback_query.data
    context.user_data["search_settings"].sex = sex if sex != "Неважно" else None
    await _message_edit(
        message=update.effective_message,
        text=templates.ASK_AGE,
        keyboard=keyboards.AGE_KEYBOARD,
    )
    return States.AGE


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
    return States.SEARCH_SETTINGS


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
    отправляет уведомление sender о том, что лайк поставлен,
    отправляет уведомление другому пользователю о лайке
    и переводит в состояние продолжения поиска.
    """
    current_profile = context.user_data.get("current_profile")
    sender_id = update.effective_chat.id
    receiver_id = current_profile["user"]

    await api_service.send_match_request(
        sender=sender_id,
        receiver=receiver_id,
    )

    await context.bot.send_message(
        chat_id=sender_id,
        text=templates.SEND_LIKE.format(receiver_name=current_profile["name"]),
    )

    keyboard = await match_keyboards.get_view_profile_keyboard(sender_id)
    await context.bot.send_message(
        chat_id=receiver_id,
        text=match_templates.LIKE_NOTIFICATION,
        reply_markup=keyboard,
    )

    await update.effective_message.reply_text(
        text=templates.ASK_NEXT_PROFILE,
        reply_markup=keyboards.NEXT_PROFILE,
    )
    return States.NEXT_PROFILE


async def end_of_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Заканчивает ветку общения по поиску соседа.
    """
    if update.callback_query:
        await update.effective_message.delete()
    await update.effective_chat.send_message(
        text=templates.END_OF_SEARCH,
        reply_markup=ReplyKeyboardRemove(),
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
            )
        profile = user_profiles.pop()
        context.user_data["current_profile"] = asdict(profile)
        context.user_data["user_profiles"] = user_profiles

        await send_profile_info(
            update=update,
            profile=profile,
            profile_template=templates.PROFILE_DATA,
        )
        return States.PROFILE

    await update.effective_message.reply_text(
        text=templates.NO_MATCHES,
        reply_markup=keyboards.NO_MATCHES_KEYBOARD,
    )
    return States.NO_MATCHES


async def send_profile_info(
    update: Update,
    profile: UserProfile,
    profile_template: str,
):
    """Формирует и отправляет сообщение с профилем пользователя."""
    profile_dict: dict = asdict(profile)

    images = profile_dict.pop("images", None)
    profile_brief_info = profile_template.format(**profile_dict)

    if images:
        media_group = [InputMediaPhoto(file_id) for file_id in images]
        await update.effective_chat.send_media_group(
            media=media_group,
            caption=profile_brief_info,
        )
    else:
        await update.effective_chat.send_message(
            text=profile_brief_info,
        )


async def _message_edit(
    message: Message,
    text: str,
    keyboard: InlineKeyboardMarkup | None = None,
) -> None:
    """
    Функция для изменения текста и клавиатуры сообщения с ParseMode.HTML.
    """
    await message.edit_text(text=text, reply_markup=keyboard)


async def _clear_roommate_search_context(context):
    context.user_data.pop("user_profiles", None)
    context.user_data.pop("current_profile", None)
