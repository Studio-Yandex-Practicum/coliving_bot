from dataclasses import asdict

from telegram import InputMediaPhoto, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.match_requests.templates as match_templates
import conversations.roommate_search.keyboards as keyboards
import conversations.roommate_search.templates as templates
from conversations.common_functions.common_funcs import profile_required
from conversations.match_requests.constants import MatchStatus
from conversations.match_requests.profile.keyboards import get_view_profile_keyboard
from conversations.profile.templates import SHORT_PROFILE_DATA
from conversations.roommate_search.buttons import ANY_GENDER_BTN
from conversations.roommate_search.constants import SRCH_STNG_FIELD
from conversations.roommate_search.states import States
from internal_requests import api_service
from internal_requests.entities import ProfileSearchSettings, UserProfile
from utils.bot import safe_send_message


@profile_required
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало ветви общения по поиску соседа.
    Проверяет, был ли настроен поиск ранее и, в зависимости от проверки,
    переводит либо в состояние подтверждения настроек, либо в настройку поиска.
    """

    search_settings = context.user_data.get(SRCH_STNG_FIELD)
    if search_settings:
        await update.effective_message.edit_text(
            text=templates.format_search_settings_message(search_settings)
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
    search_settings = context.user_data.get(SRCH_STNG_FIELD)
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
    await update.effective_message.edit_text(
        text=templates.ASK_LOCATION, reply_markup=context.bot_data["location_keyboard"]
    )

    return States.LOCATION


async def set_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает локацию в настройках поиска.
    Переводит в состояние выбора пола соседа.
    """
    location = update.callback_query.data.split(":")[1]
    context.user_data[SRCH_STNG_FIELD] = ProfileSearchSettings(location=location)
    await update.effective_message.edit_text(
        text=templates.ASK_SEX, reply_markup=keyboards.SEX_KEYBOARD
    )
    return States.SEX


async def set_sex(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает пол соседа в настройках поиска.
    Переводит в состояние выбора возраста.
    """
    sex = update.callback_query.data
    context.user_data[SRCH_STNG_FIELD].sex = sex if sex != ANY_GENDER_BTN else None
    context.user_data["question_message"] = await update.effective_message.edit_text(
        text=templates.ASK_AGE_MIN,
        reply_markup=keyboards.AGE_RANGE_IGNORE_KEYBOARD,
    )
    return States.AGE_MIN


async def handle_age_min_button_response(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает нажатие `Неважно` для минимального возраста. Спрашивает максимальный.
    """
    del context.user_data["question_message"]
    context.user_data[SRCH_STNG_FIELD].age_min = None
    context.user_data["question_message"] = await update.effective_message.edit_text(
        text=templates.ASK_AGE_MAX,
        reply_markup=keyboards.AGE_RANGE_IGNORE_KEYBOARD,
    )
    return States.AGE_MAX


async def handle_age_min_text_response(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Запоминает минимальный возраст желаемого соседа для поиска. Спрашивает максимальный.
    """
    await context.user_data["question_message"].edit_reply_markup()
    del context.user_data["question_message"]

    context.user_data[SRCH_STNG_FIELD].age_min = context.matches[0].string

    context.user_data["question_message"] = await update.effective_message.reply_text(
        text=templates.ASK_AGE_MAX,
        reply_markup=keyboards.AGE_RANGE_IGNORE_KEYBOARD,
    )
    return States.AGE_MAX


async def handle_age_max_button_response(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает нажатие `Неважно` для максимального возраста желаемого соседа.
    Переводит диалог к подтверждению настроек поиска.
    """
    del context.user_data["question_message"]
    context.user_data[SRCH_STNG_FIELD].age_max = None
    search_settings = context.user_data.get(SRCH_STNG_FIELD)
    await update.effective_message.edit_text(
        text=templates.format_search_settings_message(search_settings)
        + "\n\n"
        + templates.ASK_SEARCH_SETTINGS,
        reply_markup=keyboards.SEARCH_SETTINGS_KEYBOARD,
    )
    return States.SEARCH_SETTINGS


async def handle_age_max_text_response(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Запоминает максимальный возраст желаемого соседа для поиска.
    Переводит диалог к подтверждению настроек поиска.
    """
    await context.user_data["question_message"].edit_reply_markup()
    del context.user_data["question_message"]

    context.user_data[SRCH_STNG_FIELD].age_max = context.matches[0].string

    search_settings = context.user_data.get(SRCH_STNG_FIELD)
    await update.effective_message.reply_text(
        text=templates.format_search_settings_message(search_settings)
        + "\n\n"
        + templates.ASK_SEARCH_SETTINGS,
        reply_markup=keyboards.SEARCH_SETTINGS_KEYBOARD,
    )
    return States.SEARCH_SETTINGS


async def handle_wrong_age(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_message(templates.AGE_ERR_MSG)
    return None


async def next_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает переход на следующий профиль соседа.
    Удаляет анкету из выборки и переводит в состояние оценки анкеты,
    либо завершает поиск, если анкет больше нет.
    """
    user_profiles = context.user_data["user_profiles"]
    state = await _get_next_user_profile(update, context, user_profiles)
    return state


async def profile_dislike(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает ДИЗЛАЙК на профиль соседа.
    """
    current_profile = context.user_data["current_profile"]
    sender_id = update.effective_chat.id
    receiver_id = current_profile.user

    await api_service.send_profile_like(
        sender=sender_id, receiver=receiver_id, status=MatchStatus.IS_REJECTED.value
    )

    return await next_profile(update, context)


async def profile_like(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает ЛАЙК на профиль соседа.
    Посылает POST запрос в API на добавление MatchRequest,
    отправляет уведомление sender о том, что лайк поставлен,
    отправляет уведомление другому пользователю о лайке
    и переводит в состояние продолжения поиска.
    """
    current_profile = context.user_data["current_profile"]
    sender_id = update.effective_chat.id
    receiver_id = current_profile.user

    like = await api_service.send_profile_like(
        sender=sender_id,
        receiver=receiver_id,
    )

    keyboard = await get_view_profile_keyboard(like, sender_id)
    await safe_send_message(
        context=context,
        chat_id=receiver_id,
        text=match_templates.LIKE_NOTIFICATION,
        reply_markup=keyboard,
    )

    await update.effective_message.reply_text(
        text=templates.PROFILE_LIKE_TEXT.format(current_profile.name),
    )
    return await next_profile(update, context)


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
        context.user_data["current_profile"] = profile
        context.user_data["user_profiles"] = user_profiles

        await send_profile_info(
            update=update,
            profile=profile,
            profile_template=SHORT_PROFILE_DATA,
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
    images = profile.images.copy()
    profile.images.clear()
    profile_dict: dict = asdict(profile)
    profile_brief_info = profile_template.format(**profile_dict)

    if images:
        media_group = [InputMediaPhoto(file.file_id) for file in images]
        await update.effective_chat.send_media_group(
            media=media_group,
            caption=profile_brief_info,
        )
    else:
        await update.effective_chat.send_message(
            text=profile_brief_info,
        )


async def _clear_roommate_search_context(context):
    context.user_data.pop("user_profiles", None)
    context.user_data.pop("current_profile", None)
