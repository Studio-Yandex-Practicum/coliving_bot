# import base64
# import random
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
    WHAT_EDIT_PROFILE_KEYBOARD,
)
from conversations.coliving.states import ColivingStates as states
from conversations.coliving.templates import (
    ABOUT_FIELD,
    BTN_BED_IN_ROOM,
    BTN_CANCEL_EDIT,
    BTN_CONFIRM,
    BTN_EDIT_ABOUT_ROOM,
    BTN_EDIT_CONTINUE,
    BTN_EDIT_LOCATION,
    BTN_EDIT_PHOTO,
    BTN_EDIT_PRICE,
    BTN_EDIT_PROFILE,
    BTN_EDIT_ROOM_TYPE,
    BTN_FILL_AGAIN,
    BTN_GO_TO_MENU,
    BTN_HIDE,
    BTN_LABEL_BED_IN_ROOM,
    BTN_LABEL_CANCEL_EDIT,
    BTN_LABEL_CONFIRM,
    BTN_LABEL_EDIT_ABOUT_ROOM,
    BTN_LABEL_EDIT_CONTINUE,
    BTN_LABEL_EDIT_LOCATION,
    BTN_LABEL_EDIT_PHOTO,
    BTN_LABEL_EDIT_PRICE,
    BTN_LABEL_EDIT_PROFILE_KEYBOARD,
    BTN_LABEL_EDIT_ROOM_TYPE,
    BTN_LABEL_FILL_AGAIN,
    BTN_LABEL_MOSCOW,
    BTN_LABEL_ROOM_IN_APPARTMENT,
    BTN_LABEL_ROOM_IN_HOUSE,
    BTN_LABEL_SPB,
    BTN_MOSCOW,
    BTN_ROOM_IN_APPARTMENT,
    BTN_ROOM_IN_HOUSE,
    BTN_ROOMMATES,
    BTN_SHOW,
    BTN_SPB,
    BTN_TRANSFER_TO,
    BTN_VIEWS,
    ERR_MSG_ABOUT_MAX_LEN,
    ERR_MSG_PRICE,
    ERR_NEED_TO_SELECT_BTN,
    ERR_PHOTO_NOT_TEXT,
    IS_VISIBLE_FIELD,
    LOCATION_FIELD,
    MAX_ABOUT_LENGTH,
    MIN_ABOUT_LENGTH,
    PRICE_FIELD,
    PROFILE_DATA,
    REPLY_BTN_HIDE,
    REPLY_BTN_SHOW,
    REPLY_MSG,
    REPLY_MSG_ASK_ABOUT,
    REPLY_MSG_ASK_LOCATION,
    REPLY_MSG_ASK_PHOTO_SEND,
    REPLY_MSG_ASK_PRICE,
    REPLY_MSG_ASK_ROOM_TYPE,
    REPLY_MSG_ASK_TO_CONFIRM,
    REPLY_MSG_ASK_TO_SHOW_PROFILE,
    REPLY_MSG_HELLO,
    REPLY_MSG_PHOTO,
    REPLY_MSG_PROFILE_NO_CHANGE,
    REPLY_MSG_PROFILE_SAVED,
    REPLY_MSG_START_CREATE_PROFILE,
    REPLY_MSG_TIME_TO_CREATE_PROFILE,
    REPLY_MSG_TITLE,
    REPLY_MSG_WHAT_TO_EDIT,
    ROOM_TYPE_FIELD,
    ROOMMATES_FIELD,
    VIEWERS_FIELD,
)
from general.validators import value_is_in_range_validator
from internal_requests import mock as api_service
from internal_requests.entities import ColivingProfile
from internal_requests.service import create_coliving


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Первое сообщение от бота при вводе команды /coliving.
    Перевод на создание профиля или просмотр профиля.
    """

    effective_chat = update.effective_chat
    await context.bot.send_message(
        chat_id=effective_chat.id, text=REPLY_MSG_HELLO
    )

    coliving_status = None
    try:
        coliving_status = await api_service.get_user_coliving_status(update)
    except Exception as error:
        raise error

    if not coliving_status.is_сoliving or False:
        await update.effective_chat.send_message(
            text=REPLY_MSG_TIME_TO_CREATE_PROFILE
        )
        await update.effective_chat.send_message(
            text=REPLY_MSG_ASK_LOCATION,
            reply_markup=LOCATION_KEYBOARD,
        )
        return states.LOCATION

    elif coliving_status.is_сoliving is True:
        user_coliving_profile = (
            await api_service.get_user_coliving_info_by_tg_id(update)
        )
        await set_profile_to_context(update, context, user_coliving_profile)
        if user_coliving_profile.is_visible is True:
            await show_coliving_profile(
                update, context, keyboard=COLIVING_PROFILE_KEYBOARD_VISIBLE
            )
        else:
            await show_coliving_profile(
                update, context, keyboard=COLIVING_PROFILE_KEYBOARD_NOT_VISIBLE
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
    context.user_data[ROOMMATES_FIELD] = user_coliving_profile.roommates
    context.user_data[VIEWERS_FIELD] = user_coliving_profile.viewers
    context.user_data[IS_VISIBLE_FIELD] = user_coliving_profile.is_visible


async def handle_coliving(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """Взаимодействие с профилем коливинга"""

    await update.effective_message.edit_reply_markup()
    call_back = update.callback_query.data

    if call_back == BTN_EDIT_PROFILE:
        await update.effective_message.reply_text(
            text=f"{REPLY_MSG}{BTN_LABEL_EDIT_PROFILE_KEYBOARD}"
        )
        await update.effective_message.reply_text(
            text=REPLY_MSG_WHAT_TO_EDIT,
            reply_markup=WHAT_EDIT_PROFILE_KEYBOARD,
        )
        return states.EDIT
    elif call_back == BTN_HIDE:
        context.user_data["is_visible"] = False
        await update.effective_message.reply_text(text=REPLY_BTN_HIDE)
        #############################################################
        # Будет ошибка
        # поэтому заглушка
        await update.effective_message.reply_text(
            text=(
                "заглушка. По идее здесь сохранение "
                "и перевод обрватно на state.COLIVING"
                "\n"
                "\n"
                "Нажмите /coliving"
            )
        )
        return ConversationHandler.END
        #############################################################
        # await save_coliving_info_to_db(update, context)
        # return states.COLIVING

    elif call_back == BTN_SHOW:
        context.user_data["is_visible"] = True
        await update.effective_message.reply_text(text=REPLY_BTN_SHOW)
        #############################################################
        # Будет ошибка
        # поэтому заглушка
        await update.effective_message.reply_text(
            text=(
                "Заглушка. По идее здесь сохранение "
                "и перевод обрватно на state.COLIVING"
                "\n"
                "\n"
                "Нажмите /coliving"
            )
        )
        return ConversationHandler.END
        #############################################################
        # await save_coliving_info_to_db(update, context)
        # return states.COLIVING

    elif call_back == BTN_ROOMMATES:
        #############################################################
        # запрос к API
        # заглушка
        await update.effective_message.reply_text(
            text=(
                "Заглушка. По идее здесь запрос к API "
                "вывод списка соседей"
                "\n"
                "\n"
                "Нажмите /coliving"
            )
        )
        #############################################################
        return ConversationHandler.END

    elif call_back == BTN_VIEWS:
        #############################################################
        # запрос к API
        # заглушка
        await update.effective_message.reply_text(
            text=(
                "Заглушка. По идее здесь запрос к API "
                "вывод списка профилей тех кто лайкнул"
                "\n"
                "\n"
                "Нажмите /coliving"
            )
        )

        #############################################################
        return ConversationHandler.END

    elif call_back == BTN_TRANSFER_TO:
        #############################################################
        # заглушка
        await update.effective_message.reply_text(
            text=(
                "Заглушка. Предусмотрена передача коливинга "
                "другому владельцу"
                "\n"
                "\n"
                "Нажмите /coliving"
            )
        )
        # await set_new_ownner(update, context)
        #############################################################
        return ConversationHandler.END

    elif call_back == BTN_GO_TO_MENU:
        #############################################################
        # states.MENU
        # заглушка
        await update.effective_message.reply_text(
            text=(
                "Заглушка. По идее здесь переход "
                "в МЕНЮ на state.MENU"
                "\n"
                "\n"
                "Нажмите /coliving"
            )
        )
        # return states.MENU
        #############################################################
        return ConversationHandler.END


async def handle_location(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Выбор location и запись в контекст."""

    try:
        location = update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(
            ERR_NEED_TO_SELECT_BTN,
        )
        await update.effective_chat.send_message(
            text=REPLY_MSG_ASK_LOCATION,
            reply_markup=LOCATION_KEYBOARD,
        )
        return states.LOCATION
    await update.effective_message.edit_reply_markup()
    call_back = update.callback_query.data
    if call_back == BTN_MOSCOW:
        location = BTN_LABEL_MOSCOW
    elif call_back == BTN_SPB:
        location = BTN_LABEL_SPB
    context.user_data["location"] = location
    await update.effective_message.reply_text(text=f"{REPLY_MSG}{location}")
    await update.effective_message.reply_text(
        text=REPLY_MSG_ASK_ROOM_TYPE, reply_markup=ROOM_TYPE_KEYBOARD
    )
    return states.ROOM_TYPE


async def handle_room_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Выбор room_type и запись в контекст."""

    try:
        room_type = update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(
            ERR_NEED_TO_SELECT_BTN,
        )
        await update.effective_chat.send_message(
            text=REPLY_MSG_ASK_ROOM_TYPE, reply_markup=ROOM_TYPE_KEYBOARD
        )
        return states.ROOM_TYPE

    await update.effective_message.edit_reply_markup()
    call_back = update.callback_query.data

    if call_back == BTN_BED_IN_ROOM:
        room_type = BTN_LABEL_BED_IN_ROOM
    if call_back == BTN_ROOM_IN_APPARTMENT:
        room_type = BTN_LABEL_ROOM_IN_APPARTMENT
    if call_back == BTN_ROOM_IN_HOUSE:
        room_type = BTN_LABEL_ROOM_IN_HOUSE

    context.user_data["room_type"] = room_type
    await update.effective_message.reply_text(text=f"{REPLY_MSG}{room_type}")
    await update.effective_message.reply_text(
        text=REPLY_MSG_ASK_ABOUT,
    )
    return states.ABOUT_ROOM


async def handle_about_coliving(update, context):
    """Сохранение контекста about. Перевод на ввод PRICE."""

    about_coliving = update.message.text
    if not await value_is_in_range_validator(
        update,
        context,
        len(about_coliving),
        min=MIN_ABOUT_LENGTH,
        max=MAX_ABOUT_LENGTH,
        message=ERR_MSG_ABOUT_MAX_LEN.format(max=MAX_ABOUT_LENGTH),
    ):
        await update.effective_message.reply_text(
            text=REPLY_MSG_ASK_ABOUT,
        )
        return states.ABOUT_ROOM

    context.user_data["about"] = about_coliving
    await update.effective_message.reply_text(
        text=f"{REPLY_MSG}{about_coliving}"
    )
    await update.effective_message.reply_text(
        text=REPLY_MSG_ASK_PRICE,
    )
    return states.PRICE


async def handle_price(update, context):
    """Сохранение контекста price. Перевод на выбор PHOTO."""

    try:
        price = int(update.message.text)
    except ValueError:
        await update.effective_message.reply_text(text=ERR_MSG_PRICE)
        return states.PRICE
    message_text = update.message.text
    context.user_data["price"] = message_text
    await update.effective_message.reply_text(text=f"{REPLY_MSG}{price}")
    await update.effective_message.reply_text(
        text=REPLY_MSG_ASK_PHOTO_SEND,
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


# await photo_files.download_to_drive(
#     f'{path}/{effective_chat.first_name}_room_photo.jpg')
# await update.message.reply_text(
#     REPLY_MSG_PHOTO
# )
#     return await show_coliving_profile(update, context)


async def handle_photo_room(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Сохраняет фото."""
    # пока сохраняем одну фотку.
    if update.message.text:
        await update.effective_message.reply_text(text=ERR_PHOTO_NOT_TEXT)
        return states.PHOTO_ROOM

    effective_chat = update.effective_chat
    path = f"media/{update.effective_chat.id}/photos"
    Path(path).mkdir(parents=True, exist_ok=True)
    photo_file = await update.message.photo[-1].get_file()

    await photo_file.download_to_drive(
        f"{path}/{effective_chat.first_name}_room_photo.jpg"
    )

    ######################################################
    # Так загрузит 6 фоток и 6 раз ответит

    # await photo_file.download_to_drive(
    #     f'{path}/{effective_chat.first_name}_{photo_file.file_unique_id}.jpg'
    # )
    ######################################################

    # with open(
    #     f'{path}/{effective_chat.first_name}_{photo_file.file_unique_id}.jpg',
    #     'w',
    #     encoding='utf-8'
    # ) as image:
    #     image.write(file)

    # await update.message.reply_text(
    #     REPLY_MSG_PHOTO
    # )
    # return await show_coliving_profile(update, context)
    return await send_photo_reply(update, context)


async def send_photo_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сообщение перед просмотром профиля."""

    await update.message.reply_text(REPLY_MSG_PHOTO)
    # return await show_coliving_profile(update, context)
    await show_coliving_profile(
        update, context, keyboard=CONFIRM_OR_EDIT_PROFILE_KEYBOARD
    )
    return states.CONFIRMATION


async def show_coliving_profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    keyboard: str,
):
    """Просмотр профиля и переводит на подтверждение профиля CONFIRMATION."""

    effective_chat = update.effective_chat
    ask_to_confirm = REPLY_MSG_ASK_TO_CONFIRM
    await context.bot.sendPhoto(
        chat_id=update.effective_chat.id,
        photo=(
            f"media/{update.effective_chat.id}/photos/{effective_chat.first_name}"
            "_room_photo.jpg"
        ),
        caption=REPLY_MSG_TITLE
        + "\n"
        + PROFILE_DATA.format(
            location=context.user_data.get(LOCATION_FIELD),
            room_type=context.user_data.get(ROOM_TYPE_FIELD),
            about=context.user_data.get(ABOUT_FIELD),
            price=context.user_data.get(PRICE_FIELD),
            is_visible=False,
        )
        + "\n"
        + ask_to_confirm,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )


async def handle_confirm_or_edit_profile(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Подтверждение или изменение профиля.
    Отправка на изменение EDIT или
    на уставновку флажка поиска IS_VISIBLE.
    """

    try:
        update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(
            ERR_NEED_TO_SELECT_BTN,
        )
        await show_coliving_profile(
            update, context, keyboard=CONFIRM_OR_EDIT_PROFILE_KEYBOARD
        )
        return states.CONFIRMATION

    await update.effective_message.edit_reply_markup()
    call_back = update.callback_query.data

    if call_back == BTN_EDIT_PROFILE:
        await update.effective_message.reply_text(
            text=f"{REPLY_MSG}{BTN_LABEL_EDIT_PROFILE_KEYBOARD}"
        )
        await update.effective_message.reply_text(
            text=REPLY_MSG_WHAT_TO_EDIT,
            reply_markup=WHAT_EDIT_PROFILE_KEYBOARD,
        )
        return states.EDIT

    elif call_back == BTN_CONFIRM:
        await update.effective_message.reply_text(
            text=f"{REPLY_MSG} {BTN_LABEL_CONFIRM}"
        )
        await update.effective_message.reply_text(
            text=REPLY_MSG_ASK_TO_SHOW_PROFILE,
            reply_markup=IS_VISIBLE_OR_NOT_PROFILE_KEYBOARD,
        )
        return states.IS_VISIBLE


async def handle_is_visible_coliving_profile(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Показать или скрыть профиль в поиске и
    перевод на стадию сохранения в БД.
    """

    try:
        update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(
            ERR_NEED_TO_SELECT_BTN,
        )
        await update.effective_message.reply_text(
            text=REPLY_MSG_ASK_TO_SHOW_PROFILE,
            reply_markup=IS_VISIBLE_OR_NOT_PROFILE_KEYBOARD,
        )
        return states.IS_VISIBLE

    await update.effective_message.edit_reply_markup()
    call_back = update.callback_query.data

    if call_back == BTN_HIDE:
        context.user_data["is_visible"] = False
        await update.effective_message.reply_text(text=REPLY_BTN_HIDE)

    elif call_back == BTN_SHOW:
        context.user_data["is_visible"] = True
        await update.effective_message.reply_text(text=REPLY_BTN_SHOW)

    return await save_coliving_info_to_db(update, context)

    # context.user_data.clear()
    # return ConversationHandler.END


async def handle_what_to_edit(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Выбор редактируемого поля."""

    try:
        update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(text=ERR_NEED_TO_SELECT_BTN)
        await update.effective_message.reply_text(
            text=REPLY_MSG_WHAT_TO_EDIT,
            reply_markup=WHAT_EDIT_PROFILE_KEYBOARD,
        )
        return states.EDIT

    await update.effective_message.edit_reply_markup()
    call_back = update.callback_query.data

    if call_back == BTN_FILL_AGAIN:
        await update.effective_message.reply_text(
            text=f"{REPLY_MSG}{BTN_LABEL_FILL_AGAIN}"
        )
        context.user_data.clear()
        await update.effective_chat.send_message(
            text=REPLY_MSG_ASK_LOCATION,
            reply_markup=LOCATION_KEYBOARD,
        )
        return states.LOCATION

    elif call_back == BTN_EDIT_LOCATION:
        await update.effective_message.reply_text(
            text=f"{REPLY_MSG}{BTN_LABEL_EDIT_LOCATION}"
        )
        await update.effective_chat.send_message(
            text=REPLY_MSG_ASK_LOCATION, reply_markup=LOCATION_KEYBOARD
        )
        return states.EDIT_LOCATION

    elif call_back == BTN_EDIT_ROOM_TYPE:
        await update.effective_message.reply_text(
            text=f"{REPLY_MSG}{BTN_LABEL_EDIT_ROOM_TYPE}"
        )
        await update.effective_chat.send_message(
            text=REPLY_MSG_ASK_ROOM_TYPE, reply_markup=ROOM_TYPE_KEYBOARD
        )
        return states.EDIT_ROOM_TYPE

    elif call_back == BTN_EDIT_ABOUT_ROOM:
        await update.effective_message.reply_text(
            text=f"{REPLY_MSG}{BTN_LABEL_EDIT_ABOUT_ROOM}"
        )
        await update.effective_message.reply_text(
            text=REPLY_MSG_ASK_ABOUT,
        )
        return states.EDIT_ABOUT_ROOM

    elif call_back == BTN_EDIT_PRICE:
        await update.effective_message.reply_text(
            text=f"{REPLY_MSG}{BTN_LABEL_EDIT_PRICE}"
        )
        await update.effective_message.reply_text(
            text=REPLY_MSG_ASK_PRICE,
        )
        return states.EDIT_PRICE

    elif call_back == BTN_EDIT_PHOTO:
        await update.effective_message.reply_text(
            text=f"{REPLY_MSG}{BTN_LABEL_EDIT_PHOTO}"
        )
        await update.effective_message.reply_text(
            text=REPLY_MSG_ASK_PHOTO_SEND,
        )
        return states.EDIT_PHOTO_ROOM


async def handle_edit_location(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Редактирование location."""

    try:
        location = update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(
            ERR_NEED_TO_SELECT_BTN,
        )
        await update.effective_chat.send_message(
            text=REPLY_MSG_ASK_LOCATION,
            reply_markup=LOCATION_KEYBOARD,
        )
        return states.EDIT_LOCATION

    await update.effective_message.edit_reply_markup()
    call_back = update.callback_query.data
    if call_back == BTN_MOSCOW:
        location = BTN_LABEL_MOSCOW
    elif call_back == BTN_SPB:
        location = BTN_LABEL_SPB
    context.user_data["location"] = location
    await update.effective_message.reply_text(text=f"{REPLY_MSG}{location}")
    await show_coliving_profile(update, context, EDIT_CONFIRMATION_KEYBOARD)
    return states.EDIT_CONFIRMATION


async def handle_edit_select_room_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Редактирование типа помещения."""

    try:
        room_type = update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(
            ERR_NEED_TO_SELECT_BTN,
        )
        await update.effective_message.reply_text(
            text=REPLY_MSG_ASK_ROOM_TYPE, reply_markup=ROOM_TYPE_KEYBOARD
        )
        return states.EDIT_ROOM_TYPE

    await update.effective_message.edit_reply_markup()
    call_back = update.callback_query.data

    if call_back == BTN_BED_IN_ROOM:
        room_type = BTN_LABEL_BED_IN_ROOM

    elif call_back == BTN_ROOM_IN_APPARTMENT:
        room_type = BTN_LABEL_ROOM_IN_APPARTMENT

    elif call_back == BTN_ROOM_IN_HOUSE:
        room_type = BTN_LABEL_ROOM_IN_HOUSE

    context.user_data["room_type"] = room_type
    await update.effective_message.reply_text(text=f"{REPLY_MSG}{room_type}")
    await show_coliving_profile(update, context, EDIT_CONFIRMATION_KEYBOARD)
    return states.EDIT_CONFIRMATION


async def handle_edit_about_coliving(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Редактирование описания коливинга."""

    about_coliving = update.message.text
    if not await value_is_in_range_validator(
        update,
        context,
        len(about_coliving),
        min=MIN_ABOUT_LENGTH,
        max=MAX_ABOUT_LENGTH,
        message=ERR_MSG_ABOUT_MAX_LEN.format(max=MAX_ABOUT_LENGTH),
    ):
        await update.effective_message.reply_text(
            text=REPLY_MSG_ASK_ABOUT,
        )
        return states.EDIT_ABOUT_ROOM

    about_coliving = update.message.text
    context.user_data["about"] = about_coliving
    await update.effective_message.reply_text(
        text=f"{REPLY_MSG}{about_coliving}"
    )
    await show_coliving_profile(update, context, EDIT_CONFIRMATION_KEYBOARD)
    return states.EDIT_CONFIRMATION


async def handle_edit_price(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Редактирование цены коливинга."""

    try:
        message_text = int(update.message.text)
    except ValueError:
        await update.effective_message.reply_text(text=ERR_MSG_PRICE)
        return states.EDIT_PRICE
    context.user_data["price"] = message_text
    await update.effective_message.reply_text(
        text=f"{REPLY_MSG}{message_text}"
    )
    await show_coliving_profile(update, context, EDIT_CONFIRMATION_KEYBOARD)
    return states.EDIT_CONFIRMATION


async def handle_edit_photo_room(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Редактирование фото помещения."""

    if update.message.text:
        await update.effective_message.reply_text(text=ERR_PHOTO_NOT_TEXT)
        return states.EDIT_PHOTO_ROOM

    effective_chat = update.effective_chat
    path = f"media/{update.effective_chat.id}/photos"
    Path(path).mkdir(parents=True, exist_ok=True)
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive(
        f"{path}/{effective_chat.first_name}_room_photo.jpg"
    )
    await show_coliving_profile(update, context, EDIT_CONFIRMATION_KEYBOARD)
    return states.EDIT_CONFIRMATION


async def handle_edit_profile_confirmation(
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

    if call_back == BTN_CONFIRM:
        message = BTN_LABEL_CONFIRM
        await update.effective_message.reply_text(text=f"{REPLY_MSG}{message}")
        return await save_coliving_info_to_db(update, context)

    elif call_back == BTN_CANCEL_EDIT:
        message = BTN_LABEL_CANCEL_EDIT
        await update.effective_message.reply_text(text=f"{REPLY_MSG}{message}")
        await update.effective_message.reply_text(
            text=REPLY_MSG_PROFILE_NO_CHANGE,
        )
        context.user_data.clear()
        ########################################
        # Куда отправить?
        await update.effective_message.reply_text(
            text=REPLY_MSG_START_CREATE_PROFILE,
        )
        ########################################
        return ConversationHandler.END

    elif call_back == BTN_EDIT_CONTINUE:
        message = BTN_LABEL_EDIT_CONTINUE
        await update.effective_message.reply_text(text=f"{REPLY_MSG}{message}")
        await update.effective_message.reply_text(
            text=REPLY_MSG_WHAT_TO_EDIT,
            reply_markup=WHAT_EDIT_PROFILE_KEYBOARD,
        )
        return states.EDIT


async def save_coliving_info_to_db(
    update: Update, context: ContextTypes.DEFAULT_TYPE
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
    await update.effective_message.reply_text(text=REPLY_MSG_PROFILE_SAVED)
    context.user_data.clear()
    return ConversationHandler.END
