from dataclasses import asdict
from typing import List

from telegram import InputMediaPhoto, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes

import conversations.coliving_search.keyboards as keyboards
import conversations.coliving_search.states as states
import conversations.coliving_search.templates as templates
from conversations.coliving.constants import MAX_PRICE, MIN_PRICE
from conversations.coliving_search import constants
from general.validators import value_is_in_range_validator
from internal_requests import api_service
from internal_requests.entities import Coliving, ColivingSearchSettings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало ветви общения по поиску коливинга.
    Проверяет, был ли настроен поиск ранее и, в зависимости от проверки,
    переводит либо в состояние подтверждения настроек, либо в настройку поиска.

    """
    search_settings = context.user_data.get(constants.SRCH_STNG_FIELD)
    if search_settings:
        await update.effective_message.edit_text(
            text=templates.format_search_settings_message(search_settings)
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
    Получает список подходящих объявлений и переводит в состояние оценки коливинга.
    """
    search_settings = context.user_data.get(constants.SRCH_STNG_FIELD)
    colivings = await api_service.get_filtered_colivings(
        filters=search_settings, viewer=update.effective_chat.id
    )
    state = await _get_next_coliving(update, context, colivings)
    return state


async def edit_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Запускает процесс настройки поиска при запросе на изменение.
    Переводит в состояние выбора локации.
    """
    await _clear_coliving_search_context(context)
    await update.effective_message.delete()
    await update.effective_chat.send_message(
        text=templates.SEARCH_START,
        reply_markup=ReplyKeyboardRemove(),
    )
    await update.effective_message.reply_text(
        text=templates.ASK_LOCATION,
        reply_markup=context.bot_data["location_keyboard"],
    )
    return states.LOCATION


async def set_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает локацию в настройках поиска.
    Переводит в состояние выбора типа жилья.
    """
    location = update.callback_query.data.split(":")[1]
    context.user_data[constants.SRCH_STNG_FIELD] = ColivingSearchSettings(
        location=location
    )
    await update.effective_message.edit_text(
        text=templates.ASK_ROOM_TYPE,
        reply_markup=keyboards.ROOM_TYPE_KEYBOARD,
    )

    return states.ROOM_TYPE


async def set_room_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает тип жилья в настройках поиска.
    Переводит в состояние ввода минимальной цены.
    """
    context.user_data[constants.SRCH_STNG_FIELD].room_type = update.callback_query.data
    await update.effective_message.reply_text(
        text=templates.ASK_MIN_PRICE,
    )
    await update.effective_message.reply_text(text=templates.ASK_MIN_PRICE)

    return states.COST_MIN


async def set_cost_min(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает минимальную стоимость в настройках поиска.
    Переводит в состояние выбора максимальной стоимости.
    """
    min_price = update.message.text
    if not await value_is_in_range_validator(
        update,
        context,
        min_price,
        min=MIN_PRICE,
        max=MAX_PRICE,
        message=templates.ERR_MSG_ABOUT_COST.format(min=MIN_PRICE, max=MAX_PRICE),
    ):
        await update.effective_message.reply_text(text=templates.ASK_MIN_PRICE)
        return states.COST_MIN

    context.user_data[constants.SRCH_STNG_FIELD].min_price = min_price
    await update.effective_message.reply_text(text=templates.ASK_MAX_PRICE)
    return states.COST_MAX


async def set_cost_max(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает максимальную стоимость в настройках поиска.
    Переводит в состояние подтверждения настроек поиска.
    """
    max_price = update.message.text
    min_price = int(context.user_data[constants.SRCH_STNG_FIELD].min_price)
    if not await value_is_in_range_validator(
        update,
        context,
        max_price,
        min=min_price,
        max=MAX_PRICE,
        message=templates.ERR_MSG_ABOUT_COST.format(min=min_price, max=MAX_PRICE),
    ):
        await update.effective_message.reply_text(text=templates.ASK_MAX_PRICE)
        return states.COST_MAX

    context.user_data[constants.SRCH_STNG_FIELD].max_price = max_price
    search_settings = context.user_data.get(constants.SRCH_STNG_FIELD)

    await update.effective_message.reply_text(
        text=templates.format_search_settings_message(search_settings),
    )

    await update.effective_message.reply_text(
        text=templates.ASK_SEARCH_SETTINGS,
        reply_markup=keyboards.SEARCH_SETTINGS_KEYBOARD,
    )
    return states.SEARCH_SETTINGS


async def next_coliving(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает переход на следующий коливинг.
    Удаляет объявление из выборки и переводит в состояние оценки объявления,
    либо завершает поиск, если объявлений больше нет.
    """
    colivings = context.user_data["colivings"]
    state = await _get_next_coliving(update, context, colivings)
    return state


async def coliving_like(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает ЛАЙК на объявление коливинга.
    Посылает POST запрос в API на добавление MatchRequest,
    отправляет уведомление другому пользователю о лайке
    и переводит в состояние продолжения поиска.
    """
    current_coliving = context.user_data.get("current_coliving")
    await api_service.send_match_request(
        sender=update.effective_chat.id, receiver=current_coliving["host"]
    )

    await update.effective_message.reply_text(
        text=templates.ASK_NEXT_COLIVING,
        reply_markup=keyboards.NEXT_COLIVING,
    )
    return states.NEXT_COLIVING


async def _get_next_coliving(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    colivings: List[Coliving],
) -> int:
    """
    Функция для получения и вывода для оценки пользователю объявления из списка
     объявлений. Если объявления заканчиваются - перевод в соответствующие состояние.
    """
    if update.callback_query:
        await update.effective_message.delete()
    if colivings:
        if context.user_data.get("current_coliving") is None:
            await update.effective_chat.send_message(
                text=templates.SEARCH_INTRO,
                reply_markup=keyboards.COLIVING_KEYBOARD,
            )
        coliving = asdict(colivings.pop())
        context.user_data["current_coliving"] = coliving
        context.user_data["colivings"] = colivings
        images = coliving.get("images", [])
        message_text = templates.COLIVING_DATA.format(**coliving)
        if images:
            media_group = [InputMediaPhoto(file_id) for file_id in images]
            await update.effective_chat.send_media_group(
                media=media_group,
                caption=message_text,
            )
        else:
            await update.effective_chat.send_message(
                text=message_text,
                reply_markup=keyboards.COLIVING_KEYBOARD,
            )
        return states.COLIVING

    await update.effective_message.reply_text(
        text=templates.NO_MATCHES,
        reply_markup=keyboards.NO_MATCHES_KEYBOARD,
    )

    return states.NO_MATCHES


async def _clear_coliving_search_context(context):
    context.user_data.pop("colivings", None)
    context.user_data.pop("current_coliving", None)
