from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from conversations.coliving.keyboards import (CONFIRM_OR_EDIT_PROFILE_KEYBOARD,
                                              LOCATION_KEYBOARD,
                                              ROOM_TYPE_KEYBOARD,
                                              CONFIRMATION_KEYBOARD,
                                              CANCEL_KEYBOARD)
from conversations.coliving.states import ColivingStates as states
from conversations.coliving.templates import (LOCATION_MOSCOW_BTN_TEXT, LOCATION_SPB_BTN_TEXT,
                                              PRICE_ERR_MSG, PROFILE_DATA)
from internal_requests import mock as api_service
# from internal_requests.entities import ColivingProfile


LOCATION_FIELD = 'location'
ROOM_TYPE_FIELD = 'room_type'
ABOUT_FIELD = 'about'
PRICE_FIELD = 'price'


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
        # reply_markup = CONFIRMATION_KEYBOARD CANCEL_KEYBOARD
        await update.effective_chat.send_message(
            text='Где организован коливинг? ',
            reply_markup=LOCATION_KEYBOARD,
            # reply_markup=CONFIRMATION_KEYBOARD CANCEL_KEYBOARD,
        )
        return states.LOCATION

    elif coliving_status.is_сoliving == True:
        user_coliving_profile = await api_service.get_user_coliving_info_by_tg_id(update)
        # print(user_coliving_profile)
        await update.effective_chat.send_message(
            text=f'Ваш профиль коливинга \n{user_coliving_profile} '
        )

        # return states.LOCATION


async def select_moscow_location(update: Update, context):
    message_text = 'Москва'
    context.user_data['location'] = message_text
    return await _send_answer(message_text, update)


async def select_spb_location(update: Update, context):
    message_text = 'Санкт-Петербург'
    context.user_data['location'] = message_text
    return await _send_answer(message_text, update)


async def _send_answer(message_text, update):
    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=f'Ваш ответ: {message_text}'
    )
    await update.effective_message.reply_text(
        text='Укажите тип помещения ?',
        reply_markup=ROOM_TYPE_KEYBOARD
    )
    return states.ROOM_TYPE
    # return ConversationHandler.END

async def select_bed_in_room_type(update: Update, context):
    message_text = 'Спальное место в комнате'
    context.user_data['room_type'] = message_text
    return await _send_answer_room_type(message_text, update)


async def select_room_in_apartment_type(update: Update, context):
    message_text = 'Комната в квартире'
    context.user_data['room_type'] = message_text
    return await _send_answer_room_type(message_text, update)


async def select_room_in_house_type(update: Update, context):
    message_text = 'Комната в доме'
    context.user_data['room_type'] = message_text
    return await _send_answer_room_type(message_text, update)


async def _send_answer_room_type(message_text, update):
    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=f'Ваш ответ: {message_text}'
    )
    await update.effective_message.reply_text(
        text=('Расскажи о своей квартире.' '\n'
              'краткое описание коливинга и его жильцов ?'),
    )
    return states.ABOUT_ROOM


async def about_coliving(update, context):
    message_text = update.message.text.strip()

    context.user_data['about'] = message_text
    await update.effective_message.reply_text(
        text=f'Ваш ответ: {message_text}'
    )
    await update.effective_message.reply_text(
        text=('Укажите цену спального места за сутки?'),
        )

    return states.PRICE


async def price(update, context):
    try:
        message_text = int(update.message.text)
    except ValueError:
        await update.effective_message.reply_text(
            text=PRICE_ERR_MSG
        )
        return states.PRICE
    # message_text = update.message.text.strip()
    context.user_data['price'] = message_text
    await update.effective_message.reply_text(
        text=f'Ваш ответ: {message_text}'
    )
    await update.effective_message.reply_text(
        text=('Теперь можете отправить фото, квартиры. ' '\n'
              'Пожалуйста, загрузите до 5 фотографий'),
        )

    return states.PHOTO_ROOM
    # return ConversationHandler.END


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохраняет фото и ."""
    # user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive('user_photo.jpg')
    await update.message.reply_text(
        'О, классная квартира. ' '\n'
        'Давай взглянем на то, как выглядит твой коливинг:'
    )
    await show_coliving_profile(update, context)


async def show_coliving_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    ask_to_confirm = 'Всё верно?'
    await context.bot.send_message(
        chat_id=effective_chat.id,
        text='Твоя анкета: ' '\n'
        + '\n'
        + PROFILE_DATA.format(
            location=context.user_data.get(LOCATION_FIELD),
            room_type=context.user_data.get(ROOM_TYPE_FIELD),
            about=context.user_data.get(ABOUT_FIELD),
            price=context.user_data.get(PRICE_FIELD),
        )
        + '\n'
        + ask_to_confirm,
        parse_mode=ParseMode.HTML,
        reply_markup=CONFIRM_OR_EDIT_PROFILE_KEYBOARD
    )



#     return ConversationHandler.END
