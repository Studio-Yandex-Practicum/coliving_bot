import logging

from httpx import HTTPStatusError, codes
from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

# from internal_requests.mock import get_user_coliving_by_tg_id

from conversations.coliving.keyboards import (LOCATION_KEYBOARD,
                                              ROOM_TYPE_KEYBOARD)
from .states import ColivingStates as states
from .templates import LOCATION_MOSCOW_BTN_TEXT, LOCATION_SPB_BTN_TEXT
from internal_requests import mock as api_service


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Первое сообщение от бота при вводе команды /coliving."""
    effective_chat = update.effective_chat
    await context.bot.send_message(
        chat_id=effective_chat.id,
        text='Привет! давай проверим твой коливинг'
    )

    coliving_status = None
    try:
        coliving_status = await api_service.get_user_coliving_status(update)
    except Exception as error:
        raise error

    if not coliving_status.is_сoliving or False:
        await update.effective_chat.send_message(
            text=('Ууупс, похоже у вас еще не создан коливинг! ' '\n'
                  'Самое время создать профиль! ')
        )
        await update.effective_chat.send_message(
            text='Где организован коливинг? ',
            reply_markup=LOCATION_KEYBOARD,
        )
        return states.LOCATION

    elif coliving_status.is_сoliving == True:
        user_coliving_profile = await api_service.get_user_coliving_info_by_tg_id(update)
        # print(user_coliving_profile)
        await update.effective_chat.send_message(
            text=f'Ваш профиль коливинга \n{user_coliving_profile} '
        )

        # return states.LOCATION


async def select_moscow_location(update: Update, _context):
    message_text = 'Москва'
    _context.user_data['location'] = message_text
    return await _send_answer(message_text, update)


async def select_spb_location(update: Update, _context):
    message_text = 'Санкт-Петербург'
    _context.user_data['location'] = message_text
    return await _send_answer(message_text, update)


async def _send_answer(message_text, update):
    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(text=message_text)
    await update.effective_message.reply_text(
        text='Укажите тип помещения ?',
        reply_markup=ROOM_TYPE_KEYBOARD,
    )
    return states.ROOM_TYPE
    # return ConversationHandler.END

async def select_bed_in_room_type(update: Update, _context):
    message_text = 'Спальное место в комнате'
    _context.user_data['location'] = message_text
    return await _send_answer_room_type(message_text, update)


async def select_room_in_apartment_type(update: Update, _context):
    message_text = 'Комната в квартире'
    _context.user_data['location'] = message_text
    return await _send_answer_room_type(message_text, update)


async def select_room_in_house_type(update: Update, _context):
    message_text = 'Комната в доме'
    _context.user_data['location'] = message_text
    return await _send_answer_room_type(message_text, update)


async def _send_answer_room_type(message_text, update):
    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(text=message_text)
    await update.effective_message.reply_text(
        text=('Расскажи о своей квартире.' '\n'
              'краткое описание коливинга и его жильцов ?'),
    )
    # return states.ABOUT_ROOM
    return ConversationHandler.END






# async def select_location(
#     update: Update, context: ContextTypes.DEFAULT_TYPE
# ) -> int:
#     """
#     Обрабатывает выбранную локацию.
#     Переводит диалог в состояние ROOM_TYPE.
#     """
#     await update.effective_message.reply_text(
#         text=update.callback_query.data
#     )
#     await update.effective_message.edit_reply_markup()
#     if update.effective_message.reply_text == 'moscow_city':
#         context.user_data['location'] = 'Москва'
#     elif update.effective_message.reply_text == 'spb_city':
#         context.user_data['location'] = 'Санкт-Петербург'
#     await update.effective_message.reply_text(
#         text='Укажите тип помещения ?',
#     )
#     return states.ROOM_TYPE


# async def select_location(
#     update: Update, context: ContextTypes.DEFAULT_TYPE
# ) -> int:
#     """
#     Обрабатывает выбранную локацию.
#     Переводит диалог в состояние ROOM_TYPE.
#     """
#     await update.effective_message.reply_text(
#         text=update.callback_query.data
#         # text='а ?'
#     )
#     await update.effective_message.edit_reply_markup()
#     if update.effective_message.reply_text == LOCATION_MOSCOW_BTN_TEXT:  # LOCATION_MOSCOW_KEYBOARD:
#         context.user_data['location'] = 'Москва'
#     elif update.effective_message.reply_text == LOCATION_SPB_BTN_TEXT:
#         context.user_data['location'] = 'Санкт-Петербург'
#     await update.effective_message.reply_text(
#         text='Укажите тип помещения ?',
#     )
#     return states.ROOM_TYPE