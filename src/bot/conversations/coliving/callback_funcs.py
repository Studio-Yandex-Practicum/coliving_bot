import random
import base64

from pathlib import Path

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from conversations.coliving.keyboards import (
    COLIVING_PROFILE_KEYBOARD_NOT_VISIBLE,
    COLIVING_PROFILE_KEYBOARD_VISIBLE,
    CONFIRM_OR_EDIT_PROFILE_KEYBOARD,
    EDIT_CONFIRMATION_KEYBOARD,
    IS_VISIBLE_OR_NOT_PROFILE_KEYBOARD,
    LOCATION_KEYBOARD,
    ROOM_TYPE_KEYBOARD,
    CONFIRMATION_KEYBOARD,
    CANCEL_KEYBOARD,
    WHAT_EDIT_PROFILE_KEYBOARD,
)
from conversations.coliving.states import ColivingStates as states
from conversations.coliving.templates import (LOCATION_MOSCOW_BTN_TEXT, LOCATION_SPB_BTN_TEXT,
                                              PRICE_ERR_MSG, PROFILE_DATA)
from internal_requests import mock as api_service
from internal_requests.service import create_coliving
from internal_requests.entities import ColivingProfile


IS_EDIT = 0

LOCATION_FIELD = 'location'
ROOM_TYPE_FIELD = 'room_type'
ABOUT_FIELD = 'about'
PRICE_FIELD = 'price'
IS_VISIBLE_FIELD = 'is_visible'
ROOMMATES = 'roommates'
VIEWERS = 'viewers'



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Первое сообщение от бота при вводе команды /coliving.
    Перевод на создание профиля или просмотр профиля.
    """

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
        await set_profile_to_context(update, context, user_coliving_profile)
        if user_coliving_profile.is_visible == True:
            await show_coliving_profile(
                update,
                context,
                keyboard=COLIVING_PROFILE_KEYBOARD_VISIBLE
            )
        else:
            await show_coliving_profile(
                update,
                context,
                keyboard=COLIVING_PROFILE_KEYBOARD_NOT_VISIBLE
            )
        return states.COLIVING


async def set_profile_to_context(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_coliving_profile,
) -> None:
    """Добавление информации о коливинге в контекст"""
    context.user_data[LOCATION_FIELD] = user_coliving_profile.location
    context.user_data[ROOM_TYPE_FIELD] = user_coliving_profile.room_type
    context.user_data[ABOUT_FIELD] = user_coliving_profile.about
    context.user_data[PRICE_FIELD] = user_coliving_profile.price
    context.user_data[ROOMMATES] = user_coliving_profile.roommates
    context.user_data[VIEWERS] = user_coliving_profile.viewers
    context.user_data[IS_VISIBLE_FIELD] = user_coliving_profile.is_visible


async def handle_coliving(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """Взаимодействие с профилем коливинга"""

    await update.effective_message.edit_reply_markup()
    call_back = update.callback_query.data

    if call_back == 'edit_profile':
        await update.effective_message.reply_text(
            text=f'Ваш ответ: Изменить коливинг профиль'
        )
        await update.effective_message.reply_text(
            text='Что хотите изменить?',
            reply_markup=WHAT_EDIT_PROFILE_KEYBOARD
        )
        return states.EDIT
    elif call_back == 'hide':
        context.user_data['is_visible'] = False
        await update.effective_message.reply_text(
            text=('Ваш ответ: Скрыть из поиска' '\n'
                  '\n'
                  'Анкета скрыта из поиска. '
                  'Не забудьте установить этот параметр позже, '
                  'чтобы найти соседей.')
        )
        #############################################################
        # Будет ошибка
        # поэтому заглушка
        await update.effective_message.reply_text(
            text=('заглушка. По идее здесь сохранение '
                  'и перевод обрватно на state.COLIVING' '\n'
                  '\n'
                  'Нажмите /coliving')
        )
        return ConversationHandler.END
        #############################################################
        # await save_coliving_info_to_db(update, context)
        # return states.COLIVING

    elif call_back == 'show':
        context.user_data['is_visible'] = True
        await update.effective_message.reply_text(
            text=('Ваш ответ: Показать в поиске' '\n'
                  '\n'
                  'Анкета доступна для поиска.')
        )
        #############################################################
        # Будет ошибка
        # поэтому заглушка
        await update.effective_message.reply_text(
            text=('Заглушка. По идее здесь сохранение '
                  'и перевод обрватно на state.COLIVING' '\n'
                  '\n'
                  'Нажмите /coliving')
        )
        return ConversationHandler.END
        #############################################################
        # await save_coliving_info_to_db(update, context)
        # return states.COLIVING

    elif call_back == 'roommates_profiles':
        #############################################################
        # запрос к API
        # заглушка
        await update.effective_message.reply_text(
            text=('Заглушка. По идее здесь запрос к API '
                  'вывод списка соседей' '\n'
                  '\n'
                  'Нажмите /coliving')
        )
        #############################################################
        return ConversationHandler.END

    elif call_back == 'views':
        #############################################################
        # запрос к API
        # заглушка
        await update.effective_message.reply_text(
            text=('Заглушка. По идее здесь запрос к API '
                  'вывод списка профилей тех кто лайкнул' '\n'
                  '\n'
                  'Нажмите /coliving')
        )

        #############################################################
        return ConversationHandler.END

    elif call_back == 'transfer_to':
        #############################################################
        # заглушка
        await update.effective_message.reply_text(
            text=('Заглушка. Предусмотрена передача коливинга '
                  'другому владельцу' '\n'
                  '\n'
                  'Нажмите /coliving')
        )
        # await set_new_ownner(update, context)
        #############################################################
        return ConversationHandler.END


    elif call_back == 'go_to_menu':
        #############################################################
        # states.MENU
        # заглушка
        await update.effective_message.reply_text(
            text=('Заглушка. По идее здесь переход '
                  'в МЕНЮ на state.MENU' '\n'
                  '\n'
                  'Нажмите /coliving')
        )
        # return states.MENU
        #############################################################
        return ConversationHandler.END







async def location_not_text(update: Update, context):
    """Проверка на выбор кнопки location, а не ввод текста пользователем."""

    if update.message.text:
        await update.effective_message.reply_text(
            text='Пожалуйста, выберите вариант из предложенных.'
        )
        await update.effective_chat.send_message(
            text='Где организован коливинг? ',
            reply_markup=LOCATION_KEYBOARD,
        )
        return states.LOCATION


async def select_moscow_location(update: Update, context):
    """Сохранение контекста location."""

    message_text = 'Москва'
    context.user_data['location'] = message_text
    return await _send_answer(message_text, update)


async def select_spb_location(update: Update, context):
    """Сохранение контекста location."""

    message_text = 'Санкт-Петербург'
    context.user_data['location'] = message_text
    return await _send_answer(message_text, update)


async def _send_answer(message_text, update):
    """Перевод на выбор ROOM_TYPE."""

    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=f'Ваш ответ: {message_text}'
    )
    await update.effective_message.reply_text(
        text='Укажите тип помещения ?',
        reply_markup=ROOM_TYPE_KEYBOARD
    )
    return states.ROOM_TYPE


async def room_type_not_text(update: Update, context):
    """Проверка на выбор кнопки room_type, а не ввод текста пользователем."""

    if update.message.text:
        await update.effective_message.reply_text(
            text='Пожалуйста, выберите вариант из предложенных.'
        )
        await update.effective_message.reply_text(
            text='Выберите тип помещения:',
            reply_markup=ROOM_TYPE_KEYBOARD
        )
        return states.ROOM_TYPE


async def select_bed_in_room_type(update: Update, context):
    """Сохранение контекста room_type."""

    message_text = 'Спальное место в комнате'
    context.user_data['room_type'] = message_text
    return await _send_answer_room_type(message_text, update)


async def select_room_in_apartment_type(update: Update, context):
    """Сохранение контекста room_type."""

    message_text = 'Комната в квартире'
    context.user_data['room_type'] = message_text
    return await _send_answer_room_type(message_text, update)


async def select_room_in_house_type(update: Update, context):
    """Сохранение контекста room_type."""

    message_text = 'Комната в доме'
    context.user_data['room_type'] = message_text
    return await _send_answer_room_type(message_text, update)


async def _send_answer_room_type(message_text, update):
    """Перевод на ввод описания ABOUT_ROOM."""

    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=f'Ваш ответ: {message_text}'
    )
    await update.effective_message.reply_text(
        text=('Расскажи о своей квартире.' '\n'
              'Краткое описание коливинга и его жильцов ?'),
    )
    return states.ABOUT_ROOM
    ##################

    # if IS_EDIT == 0:
    #     return states.ABOUT_ROOM

    # if IS_EDIT == 1:
    #     IS_EDIT = 0
    #     return states.EDIT_CONFIRMATION



async def about_coliving(update, context):
    """Сохранение контекста about. Перевод на ввод PRICE."""

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
    """Сохранение контекста price. Перевод на выбор PHOTO."""

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



# async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Сохраняет фото и ."""
#     # user = update.message.from_user
#     effective_chat = update.effective_chat
#     path = f'media/{update.effective_chat.id}/photos'
#     Path(path).mkdir(parents=True, exist_ok=True)
#     # photo_file = await update.message.photo[-1].get_file()
#     photo_files = await update.message.effective_attachment[-1].get_file()
#     print(photo_files)
#     # for photo in photo_files:
#     # image_name = random.randint(0, 5)


#     await photo_files.download_to_drive(f'{path}/{effective_chat.first_name}_room_photo.jpg')
#     await update.message.reply_text(
#         'О, классная квартира. ' '\n'
#         'Давай взглянем на то, как выглядит твой коливинг:'
#     )
#     return await show_coliving_profile(update, context)



async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохраняет фото."""
    # пока сохраняем одну фотку.
    if update.message.text:
        await update.effective_message.reply_text(
            text='Пожалуйста, отправьте 5 фотографий'
        )
        return states.PHOTO_ROOM

    effective_chat = update.effective_chat
    path = f'media/{update.effective_chat.id}/photos'
    Path(path).mkdir(parents=True, exist_ok=True)
    photo_file = await update.message.photo[-1].get_file()

    await photo_file.download_to_drive(f'{path}/{effective_chat.first_name}_room_photo.jpg')


    ######################################################
    # Так загрузит 6 фоток и 6 раз ответит

    # await photo_file.download_to_drive(
    #     f'{path}/{effective_chat.first_name}_{photo_file.file_unique_id}.jpg'
    # )
    ######################################################

    # with open(
    #     f'{path}/{effective_chat.first_name}_{photo_file.file_unique_id}.jpg', 'w', encoding='utf-8'
    # ) as image:
    #     image.write(file)


    # await update.message.reply_text(
    #     'О, классная квартира. ' '\n'
    #     'Давай взглянем на то, как выглядит твой коливинг:'
    # )
    # return await show_coliving_profile(update, context)
    return await send_photo_reply(update, context)


async def send_photo_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Сообщение перед просмотром профиля."""

    await update.message.reply_text(
        'О, классная квартира. ' '\n'
        'Давай взглянем на то, как выглядит твой коливинг:'
    )
    # return await show_coliving_profile(update, context)
    await show_coliving_profile(
        update,
        context,
        keyboard=CONFIRM_OR_EDIT_PROFILE_KEYBOARD
    )
    return states.CONFIRMATION


async def show_coliving_profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    keyboard: str,
):
    """Просмотр профиля и переводит на подтверждение профиля CONFIRMATION."""

    effective_chat = update.effective_chat
    ask_to_confirm = 'Всё верно?'
    await context.bot.sendPhoto(
        chat_id=update.effective_chat.id,
        photo=(
            f'media/{update.effective_chat.id}/photos/{effective_chat.first_name}_room_photo.jpg'
        ),
        caption='Твой профиль: ' '\n'
        + '\n'
        + PROFILE_DATA.format(
            location=context.user_data.get(LOCATION_FIELD),
            room_type=context.user_data.get(ROOM_TYPE_FIELD),
            about=context.user_data.get(ABOUT_FIELD),
            price=context.user_data.get(PRICE_FIELD),
            is_visible=False,
        )
        + '\n'
        + ask_to_confirm,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )



# async def show_coliving_profile(
#     update: Update,
#     context: ContextTypes.DEFAULT_TYPE
# ):
#     """Просмотр профиля и переводит на подтверждение профиля CONFIRMATION."""

#     effective_chat = update.effective_chat
#     ask_to_confirm = 'Всё верно?'
#     await context.bot.sendPhoto(
#     # await context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         photo=(
#             f'media/{update.effective_chat.id}/photos/{effective_chat.first_name}_room_photo.jpg'
#         ),
#         caption='Твой профиль: ' '\n'
#         # text='Твоя анкета: ' '\n'
#         + '\n'
#         + PROFILE_DATA.format(
#             location=context.user_data.get(LOCATION_FIELD),
#             room_type=context.user_data.get(ROOM_TYPE_FIELD),
#             about=context.user_data.get(ABOUT_FIELD),
#             price=context.user_data.get(PRICE_FIELD),
#             is_visible=False,
#         )
#         + '\n'
#         + ask_to_confirm,
#         parse_mode=ParseMode.HTML,
#         reply_markup=CONFIRM_OR_EDIT_PROFILE_KEYBOARD
#     )
#     return states.CONFIRMATION


async def confirm_or_edit_profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    Подтверждение или изменение профиля.
    Отправка на изменение EDIT или
    на уставновку флажка поиска IS_VISIBLE.
    """
    #################################################################
    # Как здесь проверить чтоб был не ввод текста,
    # а выбор кнопки?
    #################################################################
    # if update.message.text:
    #     await update.effective_message.reply_text(
    #         text='Пожалуйста, выберите вариант из предложенных.',
    #         reply_markup=CONFIRM_OR_EDIT_PROFILE_KEYBOARD
    #     )
    #     return await show_coliving_profile(update, context)
    #################################################################

    await update.effective_message.edit_reply_markup()
    call_back = update.callback_query.data

    if call_back == 'edit_profile':
        await update.effective_message.reply_text(
            text=f'Ваш ответ: Изменить коливинг профиль'
        )
        await update.effective_message.reply_text(
            text='Что хотите изменить?',
            reply_markup=WHAT_EDIT_PROFILE_KEYBOARD
        )
        return states.EDIT

    elif call_back == 'confirm':
        await update.effective_message.reply_text(
            text=f'Ваш ответ: Да, подтвердить'
        )
        await update.effective_message.reply_text(
            text=('Сделать профиль доступным для поиска? ' '\n'
                  'Этот параметр можно установить позже.'),
            reply_markup=IS_VISIBLE_OR_NOT_PROFILE_KEYBOARD
        )
        return states.IS_VISIBLE


async def is_visible_coliving_profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    Показать или скрыть профиль в поиске и
    перевод на стадию сохранения в БД.
    """

    await update.effective_message.edit_reply_markup()
    call_back = update.callback_query.data

    if call_back == 'hide':
        context.user_data['is_visible'] = False
        await update.effective_message.reply_text(
            text=('Ваш ответ: Скрыть из поиска' '\n'
                  '\n'
                  'Анкета скрыта из поиска. '
                  'Не забудьте установить этот параметр позже, '
                  'чтобы найти соседей. ')
        )
        return await save_coliving_info_to_db(update, context)

    elif call_back == 'show':
        context.user_data['is_visible'] = True
        await update.effective_message.reply_text(
            text=('Ваш ответ: Показать в поиске' '\n'
                  '\n'
                  'Анкета доступна для поиска.')
        )
        return await save_coliving_info_to_db(update, context)


    # context.user_data.clear()
    # return ConversationHandler.END


async def what_to_edit(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Выбор редактируемого поля."""

    #################################################################
    # if update.message.text:
    #   ^^^^^^^^^^^^^^^^^^^
    # AttributeError: 'NoneType' object has no attribute 'text'
    #################################################################

    # if update.message.text:
    #     await update.effective_message.reply_text(
    #         text='Пожалуйста, выберите вариант из предложенных.'
    #     )
    #     await update.effective_message.reply_text(
    #         text='Что хотите изменить?',
    #         reply_markup=WHAT_EDIT_PROFILE_KEYBOARD
    #     )
    #     return states.EDIT

    await update.effective_message.edit_reply_markup()
    call_back = update.callback_query.data

    if call_back == 'edit_fill_again':
        await update.effective_message.reply_text(
            text=f'Ваш ответ: Заполнить заново'
        )
        context.user_data.clear()
        await update.effective_chat.send_message(
            text='Где организован коливинг? ',
            reply_markup=LOCATION_KEYBOARD,
        )
        return states.LOCATION

    elif call_back == 'edit_room_type':
        # global IS_EDIT
        # IS_EDIT = 1
        await update.effective_message.reply_text(
            text=f'Ваш ответ: Тип помещения'
        )
        await update.effective_chat.send_message(
            text='Выберите тип помещения:',
            reply_markup=ROOM_TYPE_KEYBOARD
        )
        return states.EDIT_ROOM_TYPE

    elif call_back == 'edit_description':
        await update.effective_message.reply_text(
            text=f'Ваш ответ: Описание'
        )
        await update.effective_message.reply_text(
            text=('Расскажи о своей квартире.' '\n'
                  'Краткое описание коливинга и его жильцов ?'),
        )
        return states.EDIT_ABOUT_ROOM

    elif call_back == 'edit_price':
        await update.effective_message.reply_text(
            text=f'Ваш ответ: Описание'
        )
        await update.effective_message.reply_text(
            text=('Укажите цену спального места за сутки?'),
        )
        return states.EDIT_PRICE

    elif call_back == 'edit_send_photo':
        await update.effective_message.reply_text(
            text=f'Ваш ответ: Фото квартиры'
        )
        await update.effective_message.reply_text(
            text=('Теперь можете отправить фото, квартиры. ' '\n'
                  'Пожалуйста, загрузите до 5 фотографий'),
        )
        return states.EDIT_PHOTO_ROOM



async def edit_select_room_type(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Редактирование типа помещения."""

    #################################################################
    # if update.message.text:
    #   ^^^^^^^^^^^^^^^^^^^
    # AttributeError: 'NoneType' object has no attribute 'text'
    #################################################################

    # if update.message.text:
    #     await update.effective_message.reply_text(
    #         text='Пожалуйста, выберите вариант из предложенных.'
    #     )
    #     await update.effective_message.reply_text(
    #         text='Выберите тип помещения:',
    #         reply_markup=ROOM_TYPE_KEYBOARD
    #     )
    #     return states.EDIT_ROOM_TYPE

    await update.effective_message.edit_reply_markup()
    call_back = update.callback_query.data

    if call_back == 'bed_in_room':
        message_text = 'Спальное место в комнате'

    elif call_back == 'room_in_apartment':
        message_text = 'Комната в квартире'

    elif call_back == 'room_in_house':
        message_text = 'Комната в доме'

    context.user_data['room_type'] = message_text
    await update.effective_message.reply_text(
            text=f'Ваш ответ: {message_text}'
        )
    await show_coliving_profile(
        update,
        context,
        EDIT_CONFIRMATION_KEYBOARD
    )
    return states.EDIT_CONFIRMATION


async def edit_about_coliving(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Редактирование описания коливинга."""

    message_text = update.message.text.strip()
    context.user_data['about'] = message_text
    await update.effective_message.reply_text(
        text=f'Ваш ответ: {message_text}'
    )
    await show_coliving_profile(
        update,
        context,
        EDIT_CONFIRMATION_KEYBOARD
    )
    return states.EDIT_CONFIRMATION


async def edit_price(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Редактирование цены коливинга."""

    try:
        message_text = int(update.message.text)
    except ValueError:
        await update.effective_message.reply_text(
            text=PRICE_ERR_MSG
        )
        return states.EDIT_PRICE
    context.user_data['price'] = message_text
    await update.effective_message.reply_text(
        text=f'Ваш ответ: {message_text}'
    )
    await show_coliving_profile(
        update,
        context,
        EDIT_CONFIRMATION_KEYBOARD
    )
    return states.EDIT_CONFIRMATION


async def edit_photo_room(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Редактирование фото помещения."""

    if update.message.text:
        await update.effective_message.reply_text(
            text='Пожалуйста, отправьте 5 фотографий'
        )
        return states.EDIT_PHOTO_ROOM

    effective_chat = update.effective_chat
    path = f'media/{update.effective_chat.id}/photos'
    Path(path).mkdir(parents=True, exist_ok=True)
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive(
        f'{path}/{effective_chat.first_name}_room_photo.jpg'
    )
    await show_coliving_profile(
        update,
        context,
        EDIT_CONFIRMATION_KEYBOARD
    )
    return states.EDIT_CONFIRMATION


async def edit_profile_confirmation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """
    Подтверждение измененной анкеты,
    Продолжение редактирования,
    Отмена редактирования.
    """

    await update.effective_message.edit_reply_markup()
    call_back = update.callback_query.data

    # if call_back == 'confirm':
    #     await update.effective_message.reply_text(
    #         text=f'Ваш ответ: Да, подтвердить'
    #     )

    #     return await save_coliving_info_to_db(update, context)

    # elif call_back == 'cancel':
    #     await update.effective_message.reply_text(
    #         text=f'Ваш ответ: Отменить редактирование'
    #     )
    #     await update.effective_message.reply_text(
    #         text='Хорошо, анкета не изменилась.',
    #     )
    #     context.user_data.clear()
    #     ########################################
    #     # Куда отправить?
    #     await update.effective_message.reply_text(
    #         text='Для создания профиля введите /coliving.',
    #     )
    #     ########################################
    #     return ConversationHandler.END

    # elif call_back == 'continue_editing':
    #     await update.effective_message.reply_text(
    #         text=f'Ваш ответ: Продолжить редактирование'
    #     )
    #     await update.effective_message.reply_text(
    #         text='Что хотите изменить?',
    #         reply_markup=WHAT_EDIT_PROFILE_KEYBOARD
    #     )
    #     return states.EDIT


    if call_back == 'confirm':
        message = 'Да, подтвердить'
        await update.effective_message.reply_text(
            text=f'Ваш ответ: {message}'
        )
        return await save_coliving_info_to_db(update, context)

    elif call_back == 'cancel':
        message = 'Отменить редактирование'
        await update.effective_message.reply_text(
            text=f'Ваш ответ: {message}'
        )
        await update.effective_message.reply_text(
            text='Хорошо, анкета не изменилась.',
        )
        context.user_data.clear()
        ########################################
        # Куда отправить?
        await update.effective_message.reply_text(
            text='Для создания профиля введите /coliving.',
        )
        ########################################
        return ConversationHandler.END

    elif call_back == 'continue_editing':
        message = 'Продолжить редактирование'
        await update.effective_message.reply_text(
            text=f'Ваш ответ: {message}'
        )
        await update.effective_message.reply_text(
            text='Что хотите изменить?',
            reply_markup=WHAT_EDIT_PROFILE_KEYBOARD
        )
        return states.EDIT


#####
# решить что лучше выше.!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#####



























async def save_coliving_info_to_db(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> ColivingProfile:
    """
    Сохраняет в БД - запрос к API.
    Отправляет сообщение о завершении регистрации.
    """

    coliving_info = ColivingProfile(
        location=context.user_data.get(LOCATION_FIELD),
        room_type=context.user_data.get(ROOM_TYPE_FIELD),
        about=context.user_data.get(ABOUT_FIELD),
        price=context.user_data.get(PRICE_FIELD),
        is_visible=context.user_data.get(IS_VISIBLE_FIELD),
        roommates=None,
        viewers=None,
        created_date=None,

        # images=
    )
    await create_coliving(coliving=coliving_info)
    # await api_service.create_coliving(user=user_info)
    await update.effective_message.reply_text(
            text='Профиль успешно сохранен!'
        )
    context.user_data.clear()
    return ConversationHandler.END
