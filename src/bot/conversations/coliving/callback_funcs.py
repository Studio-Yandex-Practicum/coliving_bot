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
    WHAT_EDIT_PROFILE_KEYBOARD,
)
from conversations.coliving.states import ColivingStates as states
from conversations.coliving.templates import (
    ABOUT_FIELD,
    BTN_EDIT_PHOTO,
    BTN_EDIT_PROFILE,
    BTN_GO_TO_MENU,
    BTN_HIDE,
    BTN_LABEL_CANCEL_EDIT,
    BTN_LABEL_CONFIRM,
    BTN_LABEL_EDIT_ABOUT_ROOM,
    BTN_LABEL_EDIT_CONTINUE,
    BTN_LABEL_EDIT_LOCATION,
    BTN_LABEL_EDIT_PRICE,
    BTN_LABEL_EDIT_PROFILE_KEYBOARD,
    BTN_LABEL_EDIT_ROOM_TYPE,
    BTN_LABEL_FILL_AGAIN,
    BTN_ROOMMATES,
    BTN_SHOW,
    BTN_TRANSFER_TO,
    BTN_VIEWS,
    ERR_MSG_ABOUT_MAX_LEN,
    ERR_MSG_PRICE,
    ERR_NEED_TO_SELECT_BTN,
    ERR_PHOTO_NOT_TEXT,
    IMAGE_FIELD,
    IS_VISIBLE_FIELD,
    IS_VISIBLE_NO,
    IS_VISIBLE_YES,
    LOCATION_FIELD,
    MAX_ABOUT_LENGTH,
    MAX_PRICE,
    MIN_ABOUT_LENGTH,
    MIN_PRICE,
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
    Перевод на создание колинг профиля или его просмотр.
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

    if not coliving_status.is_сoliving:
        await update.effective_chat.send_message(
            text=REPLY_MSG_TIME_TO_CREATE_PROFILE
        )
        await update.effective_chat.send_message(
            text=REPLY_MSG_ASK_LOCATION,
            reply_markup=LOCATION_KEYBOARD,
        )
        return states.LOCATION

    else:
        user_coliving_profile = (
            await api_service.get_user_coliving_info_by_tg_id(update)
        )
        await set_profile_to_context(update, context, user_coliving_profile)
        if user_coliving_profile.is_visible == IS_VISIBLE_YES:
            await show_coliving_profile(
                update,
                context,
                " ",
                keyboard=COLIVING_PROFILE_KEYBOARD_VISIBLE,
            )
        else:
            await show_coliving_profile(
                update,
                context,
                " ",
                keyboard=COLIVING_PROFILE_KEYBOARD_NOT_VISIBLE,
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

    try:
        update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(
            ERR_NEED_TO_SELECT_BTN,
        )
        if context.user_data[IS_VISIBLE_FIELD] == IS_VISIBLE_YES:
            await show_coliving_profile(
                update,
                context,
                " ",
                keyboard=COLIVING_PROFILE_KEYBOARD_VISIBLE,
            )
        else:
            await show_coliving_profile(
                update,
                context,
                " ",
                keyboard=COLIVING_PROFILE_KEYBOARD_NOT_VISIBLE,
            )
        return states.COLIVING

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
        context.user_data[IS_VISIBLE_FIELD] = IS_VISIBLE_NO
        await update.effective_message.reply_text(text=REPLY_BTN_HIDE)
        await show_coliving_profile(
            update,
            context,
            " ",
            keyboard=COLIVING_PROFILE_KEYBOARD_NOT_VISIBLE,
        )
        ############################################################
        # добавить для сохранения в БД
        # await save_coliving_info_to_db(update, context)
        #
        ############################################################
        return states.COLIVING

    elif call_back == BTN_SHOW:
        context.user_data[IS_VISIBLE_FIELD] = IS_VISIBLE_YES
        await update.effective_message.reply_text(text=REPLY_BTN_SHOW)

        await show_coliving_profile(
            update, context, " ", keyboard=COLIVING_PROFILE_KEYBOARD_VISIBLE
        )
        ############################################################
        # добавить для сохранения в БД
        # await save_coliving_info_to_db(update, context)
        #
        ############################################################
        return states.COLIVING

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


async def handle_location_text_input_instead_of_choosing_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Выбор местоположения коливинг профиля.
    Проверка ввод текста или нажатие кнопки.
    """
    await update.effective_message.reply_text(
        ERR_NEED_TO_SELECT_BTN,
    )
    await update.effective_chat.send_message(
        text=REPLY_MSG_ASK_LOCATION,
        reply_markup=LOCATION_KEYBOARD,
    )


async def handle_location(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Выбор местоположения и запись в контекст."""

    location = update.callback_query.data
    await update.effective_message.edit_reply_markup()
    context.user_data[LOCATION_FIELD] = location
    await update.effective_message.reply_text(text=f"{REPLY_MSG}{location}")
    await update.effective_message.reply_text(
        text=REPLY_MSG_ASK_ROOM_TYPE, reply_markup=ROOM_TYPE_KEYBOARD
    )
    return states.ROOM_TYPE


async def handle_room_type_text_input_instead_of_choosing_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Выбор типа спального места коливинг профиля.
    Проверка ввод текста или нажатие кнопки.
    """
    await update.effective_message.reply_text(
        ERR_NEED_TO_SELECT_BTN,
    )
    await update.effective_chat.send_message(
        text=REPLY_MSG_ASK_ROOM_TYPE,
        reply_markup=ROOM_TYPE_KEYBOARD,
    )


async def handle_room_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Выбор типа спального места и запись в контекст."""

    room_type = update.callback_query.data
    await update.effective_message.edit_reply_markup()
    context.user_data[ROOM_TYPE_FIELD] = room_type
    await update.effective_message.reply_text(text=f"{REPLY_MSG}{room_type}")
    await update.effective_message.reply_text(
        text=REPLY_MSG_ASK_ABOUT,
    )
    return states.ABOUT_ROOM


async def handle_about_coliving(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Ввод описания коливинг профиля и сохранение в контекст."""

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

    context.user_data[ABOUT_FIELD] = about_coliving
    await update.effective_message.reply_text(
        text=f"{REPLY_MSG}{about_coliving}"
    )
    await update.effective_message.reply_text(
        text=REPLY_MSG_ASK_PRICE,
    )
    return states.PRICE


async def handle_price(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Ввод цены за спальное место коливинг профиля
    и сохранение в контекст.
    Перевод на стейт PHOTO_ROOM.
    """

    price = update.message.text
    if not await value_is_in_range_validator(
        update=update,
        context=context,
        value=price,
        min=MIN_PRICE,
        max=MAX_PRICE,
        message=ERR_MSG_PRICE.format(min=MIN_PRICE, max=MAX_PRICE),
    ):
        return states.PRICE

    context.user_data[PRICE_FIELD] = price
    await update.effective_message.reply_text(text=f"{REPLY_MSG}{price}")
    await update.effective_message.reply_text(
        text=REPLY_MSG_ASK_PHOTO_SEND,
    )

    return states.PHOTO_ROOM


async def encode_photo_room(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> str:
    """Кодирование изображения"""
    effective_chat = update.effective_chat
    path = f"media/{update.effective_chat.id}/photos"
    Path(path).mkdir(parents=True, exist_ok=True)
    photo_file = await update.message.photo[-1].get_file()
    # for i in range(len)
    await photo_file.download_to_drive(
        f"{path}/{effective_chat.first_name}_room_photo.jpg"
    )
    with open(
        f"{path}/{effective_chat.first_name}_room_photo.jpg", "rb"
    ) as image:
        return base64.b64encode(image.read())
    ######################################################
    # Так загрузит 6 фоток и 6 раз ответит

    # await photo_file.download_to_drive(
    #     f'{path}/{effective_chat.first_name}_{photo_file.file_unique_id}.jpg'
    # )
    ######################################################


async def handle_photo_room(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Сохраняет фото."""
    # пока сохраняем одну фотку.
    if update.message.text:
        await update.effective_message.reply_text(text=ERR_PHOTO_NOT_TEXT)
        return states.PHOTO_ROOM

    context.user_data[IMAGE_FIELD] = await encode_photo_room(update, context)
    await update.message.reply_text(REPLY_MSG_PHOTO)
    context.user_data[IS_VISIBLE_FIELD] = IS_VISIBLE_NO
    await show_coliving_profile(
        update,
        context,
        REPLY_MSG_ASK_TO_CONFIRM,
        keyboard=CONFIRM_OR_EDIT_PROFILE_KEYBOARD,
    )
    return states.CONFIRMATION


async def show_coliving_profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    ask_to_confirm,
    keyboard: str,
) -> None:
    """Просмотр профиля и переводит на подтверждение профиля CONFIRMATION."""

    effective_chat = update.effective_chat
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
            is_visible=context.user_data.get(IS_VISIBLE_FIELD),
        )
        + "\n"
        + ask_to_confirm,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )


async def handle_confirm_or_edit_profile_text_instead_of_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Подтверждение или изменение коливинг профиля.
    Проверка: ввод текста или нажатие кнопки
    """

    await update.effective_message.reply_text(
        ERR_NEED_TO_SELECT_BTN,
    )
    await show_coliving_profile(
        update,
        context,
        REPLY_MSG_ASK_TO_CONFIRM,
        keyboard=CONFIRM_OR_EDIT_PROFILE_KEYBOARD,
    )


async def handle_confirm_or_edit_reply_edit_profile(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Подтверждение или изменение коливинг профиля.
    Обработка ответа - изменение коливинг профиля.
    """
    await update.effective_message.edit_reply_markup()
    reply = BTN_LABEL_EDIT_PROFILE_KEYBOARD
    await update.effective_message.reply_text(text=f"{REPLY_MSG}{reply}")
    await update.effective_message.reply_text(
        text=REPLY_MSG_WHAT_TO_EDIT,
        reply_markup=WHAT_EDIT_PROFILE_KEYBOARD,
    )
    return states.EDIT


async def handle_confirm_or_edit_reply_confirm(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Подтверждение или изменение коливинг профиля.
    Обработка ответа - подтверждение коливинг профиля.
    Перевод на уставновку флажка поиска IS_VISIBLE.
    """
    await update.effective_message.edit_reply_markup()
    reply = BTN_LABEL_CONFIRM
    await update.effective_message.reply_text(text=f"{REPLY_MSG}{reply}")
    await update.effective_message.reply_text(
        text=REPLY_MSG_ASK_TO_SHOW_PROFILE,
        reply_markup=IS_VISIBLE_OR_NOT_PROFILE_KEYBOARD,
    )
    return states.IS_VISIBLE


async def handle_is_visible_coliving_profile_text_instead_of_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Показать или скрыть профиль в поиске.
    Проверка: ввод текста или нажатие кнопки.
    """

    await update.effective_message.reply_text(
        ERR_NEED_TO_SELECT_BTN,
    )
    await update.effective_message.reply_text(
        text=REPLY_MSG_ASK_TO_SHOW_PROFILE,
        reply_markup=IS_VISIBLE_OR_NOT_PROFILE_KEYBOARD,
    )


async def handle_is_visible_coliving_profile_no(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка ответа: скрыть профиль в поиске и
    перевод на стадию сохранения в БД.
    """

    await update.effective_message.edit_reply_markup()
    context.user_data[IS_VISIBLE_FIELD] = IS_VISIBLE_NO
    await update.effective_message.reply_text(text=REPLY_BTN_HIDE)
    return await save_coliving_info_to_db(update, context)


async def handle_is_visible_coliving_profile_yes(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка ответа: показать профиль в поиске и
    перевод на стадию сохранения в БД.
    """
    await update.effective_message.edit_reply_markup()
    context.user_data[IS_VISIBLE_FIELD] = IS_VISIBLE_YES
    await update.effective_message.reply_text(text=REPLY_BTN_SHOW)
    return await save_coliving_info_to_db(update, context)


async def handle_what_to_edit_text_instead_of_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Выбор редактируемого поля.
    Проверка: ввод текста или нажатие кнопки.
    """

    update.callback_query.data
    await update.effective_message.reply_text(text=ERR_NEED_TO_SELECT_BTN)
    await update.effective_message.reply_text(
        text=REPLY_MSG_WHAT_TO_EDIT,
        reply_markup=WHAT_EDIT_PROFILE_KEYBOARD,
    )


async def handle_what_to_edit_fill_again(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Выбор редактируемого поля.
    Обработка ответа: Заполнить заново.
    """

    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=f"{REPLY_MSG}{BTN_LABEL_FILL_AGAIN}"
    )
    context.user_data.clear()
    await update.effective_chat.send_message(
        text=REPLY_MSG_ASK_LOCATION,
        reply_markup=LOCATION_KEYBOARD,
    )
    return states.LOCATION


async def handle_what_to_edit_location(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Выбор редактируемого поля.
    Обработка ответа: Местоположение.
    """

    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=f"{REPLY_MSG}{BTN_LABEL_EDIT_LOCATION}"
    )
    await update.effective_chat.send_message(
        text=REPLY_MSG_ASK_LOCATION, reply_markup=LOCATION_KEYBOARD
    )
    return states.EDIT_LOCATION


async def handle_what_to_edit_room_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Выбор редактируемого поля.
    Обработка ответа: Тип помещения.
    """

    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=f"{REPLY_MSG}{BTN_LABEL_EDIT_ROOM_TYPE}"
    )
    await update.effective_chat.send_message(
        text=REPLY_MSG_ASK_ROOM_TYPE, reply_markup=ROOM_TYPE_KEYBOARD
    )
    return states.EDIT_ROOM_TYPE


async def handle_what_to_edit_about_room(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Выбор редактируемого поля.
    Обработка ответа: Описание.
    """

    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=f"{REPLY_MSG}{BTN_LABEL_EDIT_ABOUT_ROOM}"
    )
    await update.effective_message.reply_text(
        text=REPLY_MSG_ASK_ABOUT,
    )
    return states.EDIT_ABOUT_ROOM


async def handle_what_to_edit_price(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Выбор редактируемого поля.
    Обработка ответа: Цена.
    """

    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=f"{REPLY_MSG}{BTN_LABEL_EDIT_PRICE}"
    )
    await update.effective_message.reply_text(
        text=REPLY_MSG_ASK_PRICE,
    )
    return states.EDIT_PRICE


async def handle_what_to_edit_photo_room(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Выбор редактируемого поля.
    Обработка ответа: Фото квартиры.
    """

    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=f"{REPLY_MSG}{BTN_EDIT_PHOTO}"
    )
    await update.effective_message.reply_text(
        text=REPLY_MSG_ASK_PHOTO_SEND,
    )
    return states.EDIT_PHOTO_ROOM


async def handle_edit_location(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Редактирование location."""

    location = update.callback_query.data
    await update.effective_message.edit_reply_markup()
    context.user_data[LOCATION_FIELD] = location
    await update.effective_message.reply_text(text=f"{REPLY_MSG}{location}")
    await show_coliving_profile(
        update, context, REPLY_MSG_ASK_TO_CONFIRM, EDIT_CONFIRMATION_KEYBOARD
    )
    return states.EDIT_CONFIRMATION


async def handle_edit_select_room_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Редактирование типа помещения."""

    room_type = update.callback_query.data
    await update.effective_message.edit_reply_markup()
    context.user_data[ROOM_TYPE_FIELD] = room_type
    await update.effective_message.reply_text(text=f"{REPLY_MSG}{room_type}")
    await show_coliving_profile(
        update, context, REPLY_MSG_ASK_TO_CONFIRM, EDIT_CONFIRMATION_KEYBOARD
    )
    return states.EDIT_CONFIRMATION


async def handle_edit_about_coliving(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
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
    context.user_data[ABOUT_FIELD] = about_coliving
    await update.effective_message.reply_text(
        text=f"{REPLY_MSG}{about_coliving}"
    )
    await show_coliving_profile(
        update, context, REPLY_MSG_ASK_TO_CONFIRM, EDIT_CONFIRMATION_KEYBOARD
    )
    return states.EDIT_CONFIRMATION


async def handle_edit_price(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Редактирование цены коливинга."""

    edit_price = update.message.text
    if not await value_is_in_range_validator(
        update=update,
        context=context,
        value=edit_price,
        min=MIN_PRICE,
        max=MAX_PRICE,
        message=ERR_MSG_PRICE.format(min=MIN_PRICE, max=MAX_PRICE),
    ):
        return states.EDIT_PRICE

    context.user_data[PRICE_FIELD] = edit_price
    await update.effective_message.reply_text(text=f"{REPLY_MSG}{edit_price}")
    await show_coliving_profile(
        update, context, REPLY_MSG_ASK_TO_CONFIRM, EDIT_CONFIRMATION_KEYBOARD
    )
    return states.EDIT_CONFIRMATION


async def handle_edit_photo_room(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Редактирование фото помещения."""

    if update.message.text:
        await update.effective_message.reply_text(text=ERR_PHOTO_NOT_TEXT)
        return states.EDIT_PHOTO_ROOM

    context.user_data[IMAGE_FIELD] = await encode_photo_room(update, context)

    await show_coliving_profile(
        update, context, REPLY_MSG_ASK_TO_CONFIRM, EDIT_CONFIRMATION_KEYBOARD
    )
    return states.EDIT_CONFIRMATION


async def handle_edit_profile_confirmation_text_instead_of_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Подтверждение измененного коливинг профиля.
    Продолжение редактирования. Отмена редактирования.
    Проверка: ввод текста или нажатие кнопки.
    """

    await update.effective_message.reply_text(
        ERR_NEED_TO_SELECT_BTN,
    )
    await show_coliving_profile(
        update,
        context,
        REPLY_MSG_ASK_TO_CONFIRM,
        EDIT_CONFIRMATION_KEYBOARD,
    )


async def handle_edit_profile_confirmation_confirm(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Подтверждение измененного коливинг профиля."""

    await update.effective_message.edit_reply_markup()
    message = BTN_LABEL_CONFIRM
    await update.effective_message.reply_text(text=f"{REPLY_MSG}{message}")
    return await save_coliving_info_to_db(update, context)


async def handle_edit_profile_confirmation_cancel(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отмена редактирования коливинг профиля."""

    await update.effective_message.edit_reply_markup()
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


async def handle_edit_profile_confirmation_continue_edit(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Продолжение редактирования коливинг профиля."""

    await update.effective_message.edit_reply_markup()
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
