from dataclasses import asdict
from typing import List

from telegram import (
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
    ReplyKeyboardRemove,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import conversations.coliving_search.keyboards as keyboards
import conversations.coliving_search.states as states
import conversations.coliving_search.templates as templates
import conversations.common_functions.common_keyboards as common_keyboards
from conversations.menu.callback_funcs import menu
from general.validators import value_is_in_range_validator
from internal_requests import api_service
from internal_requests.entities import Coliving, ColivingSearchSettings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало ветви общения по поиску коливинга.
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
    Получает список подходящих объявлений и переводит в состояние оценки коливинга.
    """
    search_settings = context.user_data.get("search_settings")
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

    await _message_edit(
        message=update.effective_message,
        text=f"{templates.SEARCH_START}\n{templates.ASK_LOCATION}",
        keyboard=context.bot_data["location_keyboard"],
    )

    return states.LOCATION


async def set_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает локацию в настройках поиска.
    Переводит в состояние выбора типа жилья.
    """
    location = update.callback_query.data.split(":")[1]
    context.user_data["search_settings"] = ColivingSearchSettings(location=location)
    await _message_edit(
        message=update.effective_message,
        text=templates.ASK_ROOM_TYPE,
        keyboard=keyboards.ROOM_TYPE_KEYBOARD,
    )
    return states.ROOM_TYPE


async def set_room_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает тип жилья в настройках поиска.
    Переводит в состояние ввода минимальной цены.
    """
    context.user_data["search_settings"].room_type = update.callback_query.data
    await _message_edit(
        message=update.effective_message,
        text=templates.ASK_PRICE,
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
        int(min_price),
        min=templates.MIN_COST,
        max=templates.MAX_COST,
        message=templates.ERR_MSG_ABOUT_COST.format(
            min=templates.MIN_COST, max=templates.MAX_COST
        ),
    ):
        await update.effective_message.reply_text(
            text=templates.ASK_MIN_PRICE,
            reply_markup=common_keyboards.CANCEL_KEYBOARD,
        )
        return states.COST_MIN

    context.user_data["search_settings"].min_price = min_price
    await update.effective_message.reply_text(
        text=templates.ASK_MAX_PRICE,
    )
    return states.COST_MAX


async def set_cost_max(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Устанавливает максимальную стоимость в настройках поиска.
    Переводит в состояние подтверждения настроек поиска.
    """
    max_price = update.message.text
    min_price = int(context.user_data["search_settings"].min_price)
    if not await value_is_in_range_validator(
        update,
        context,
        int(max_price),
        min=min_price,
        max=templates.MAX_COST,
        message=templates.ERR_MSG_ABOUT_COST.format(
            min=min_price, max=templates.MAX_COST
        ),
    ):
        await update.effective_message.reply_text(
            text=templates.ASK_MAX_PRICE,
        )
        return states.COST_MAX

    context.user_data["search_settings"].max_price = max_price
    search_settings = context.user_data.get("search_settings")

    await update.effective_message.reply_text(
        text=templates.format_search_settings_message(search_settings),
        parse_mode=ParseMode.HTML,
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
        sender=update.effective_chat.id, receiver=current_coliving["id"]
    )

    await update.effective_message.reply_text(
        text=templates.ASK_NEXT_COLIVING,
        reply_markup=keyboards.NEXT_COLIVING,
        parse_mode=ParseMode.HTML,
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
                parse_mode=ParseMode.HTML,
            )
        coliving = asdict(colivings.pop())
        context.user_data["current_coliving"] = coliving
        context.user_data["colivings"] = colivings
        images = coliving.get("images", [])
        message_text = templates.COLIVING_DATA.format(**coliving)
        if images:
            media_group = [InputMediaPhoto(file_id) for file_id in images]
            await update.effective_chat.send_media_group(
                media=media_group, caption=message_text, parse_mode=ParseMode.HTML
            )
        else:
            await update.effective_chat.send_message(
                text=message_text,
                reply_markup=keyboards.COLIVING_KEYBOARD,
                parse_mode=ParseMode.HTML,
            )
        return states.COLIVING

    await update.effective_message.reply_text(
        text=templates.NO_MATCHES,
        reply_markup=keyboards.NO_MATCHES_KEYBOARD,
        parse_mode=ParseMode.HTML,
    )

    return states.NO_MATCHES


async def handle_return_to_menu_response(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка ответа: Ждать.
    """
    await _clear_coliving_search_context(context)
    await update.effective_message.delete()
    await update.effective_chat.send_message(
        text=templates.END_OF_SEARCH,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )
    await menu(update, context)
    return ConversationHandler.END


async def _message_edit(
    message: Message,
    text: str,
    keyboard: InlineKeyboardMarkup | None = None,
) -> None:
    """
    Функция для изменения текста и клавиатуры сообщения с ParseMode.HTML.
    """
    await message.edit_text(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def _clear_coliving_search_context(context):
    context.user_data.pop("colivings", None)
    context.user_data.pop("current_coliving", None)
