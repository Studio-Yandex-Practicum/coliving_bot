from typing import Optional

from telegram import InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, ContextTypes, ConversationHandler

import conversations.coliving.keyboards as keyboards
import conversations.coliving.states as states
import conversations.coliving.templates as templates
import conversations.common_functions.common_funcs as common_funcs
import conversations.common_functions.common_keyboards as common_keyboards
from conversations.coliving.templates import format_coliving_profile_message
from conversations.menu.callback_funcs import menu
from general.validators import value_is_in_range_validator
from internal_requests import api_service
from internal_requests.entities import Coliving, Image
from internal_requests.service import ColivingNotFound


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Первое сообщение от бота после нажатия кнопки Коливинг в меню.
    Перевод на создание коливинг профиля или его просмотр.
    """
    current_chat = update.effective_chat

    try:
        context.user_data[
            "coliving_info"
        ] = await api_service.get_coliving_info_by_user(telegram_id=current_chat.id)
    except ColivingNotFound:
        await update.effective_message.edit_text(
            text=templates.REPLY_MSG_TIME_TO_CREATE_PROFILE,
        )
        await current_chat.send_message(
            text=templates.REPLY_MSG_ASK_LOCATION,
            reply_markup=common_funcs.combine_keyboards(
                context.bot_data["location_keyboard"], common_keyboards.CANCEL_KEYBOARD
            ),
        )

        context.user_data["coliving_info"] = Coliving(host=update.effective_chat.id)
        return states.LOCATION

    await update.effective_message.edit_text(text=templates.REPLY_MSG_HELLO)
    await _show_coliving_profile(
        update=update,
        context=context,
        ask_to_confirm=False,
    )
    return states.COLIVING


async def handle_coliving_text_instead_of_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Проверка ввод текста или нажатие кнопки.
    Проверка статуса видимости.
    """

    await update.effective_message.reply_text(
        templates.ERR_NEED_TO_SELECT_BTN,
    )

    await _show_coliving_profile(update, context, ask_to_confirm=False)
    return states.COLIVING


async def handle_coliving_edit(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Обработка ответа: Изменить коливинг профиль."""

    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=f"{templates.REPLY_MSG}{templates.BTN_LABEL_EDIT_PROFILE_KEYBOARD}"
    )
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_WHAT_TO_EDIT,
        reply_markup=keyboards.WHAT_EDIT_PROFILE_KEYBOARD,
    )
    return states.EDIT


async def handle_is_visible_switching(update: Update, context: CallbackContext) -> int:
    """Обработка ответа: Скрыть из поиска."""
    callback_data = update.callback_query.data
    await update.effective_message.edit_reply_markup()
    context.user_data["coliving_info"].is_visible = eval(callback_data)
    if context.user_data["coliving_info"].is_visible:
        await update.effective_message.reply_text(text=templates.REPLY_BTN_SHOW)
    else:
        await update.effective_message.reply_text(text=templates.REPLY_BTN_HIDE)
    context.user_data["coliving_info"] = await api_service.update_coliving_info(
        coliving=context.user_data["coliving_info"]
    )

    await _show_coliving_profile(
        update,
        context,
        ask_to_confirm=False,
    )

    return states.COLIVING


async def handle_coliving_roommates(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Обработка ответа: Посмотреть анкеты соседей."""

    #############################################################
    # запрос к API
    # заглушка
    await update.effective_message.edit_reply_markup()
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


async def handle_coliving_views(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Обработка ответа: Просмотры."""
    #############################################################
    # запрос к API
    # заглушка
    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=(
            "Заглушка. По идее здесь запрос к API "
            "вывод списка профилей тех поставил лайк"
            "\n"
            "\n"
            "Нажмите /coliving"
        )
    )

    #############################################################
    return ConversationHandler.END


async def handle_coliving_transfer_to(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Обработка ответа: Передача коливинга."""
    #############################################################
    # заглушка
    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=(
            "Заглушка. Предусмотрена передача коливинга "
            "другому владельцу"
            "\n"
            "\n"
            "Нажмите /coliving"
        )
    )
    # await set_new_owner(update, context)
    #############################################################
    return ConversationHandler.END


async def handle_return_to_menu_response(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Обработка ответа: Вернуться в меню."""
    await update.effective_message.edit_reply_markup()
    context.user_data.clear()
    await menu(update, context)
    return ConversationHandler.END


async def handle_location_text_input_instead_of_choosing_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Выбор местоположения коливинг профиля.
    Проверка ввод текста или нажатие кнопки.
    """
    await update.effective_message.reply_text(
        templates.ERR_NEED_TO_SELECT_BTN,
    )
    await update.effective_chat.send_message(
        text=templates.REPLY_MSG_ASK_LOCATION,
        reply_markup=context.bot_data["location_keyboard"],
    )


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выбор местоположения и запись в контекст."""
    location = update.callback_query.data.split(":")[1]
    await update.effective_message.edit_reply_markup()
    context.user_data["coliving_info"].location = location
    await update.effective_message.reply_text(text=f"{templates.REPLY_MSG}{location}")
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_ASK_ROOM_TYPE,
        reply_markup=common_funcs.combine_keyboards(
            keyboards.ROOM_TYPE_KEYBOARD, common_keyboards.CANCEL_KEYBOARD
        ),
    )
    return states.ROOM_TYPE


async def handle_room_type_text_input_instead_of_choosing_button(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Выбор типа спального места коливинг профиля.
    Проверка ввод текста или нажатие кнопки.
    """
    await update.effective_message.reply_text(
        templates.ERR_NEED_TO_SELECT_BTN,
    )
    await update.effective_chat.send_message(
        text=templates.REPLY_MSG_ASK_ROOM_TYPE,
        reply_markup=keyboards.ROOM_TYPE_KEYBOARD,
    )


async def handle_room_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выбор типа спального места и запись в контекст."""
    await update.effective_message.edit_reply_markup()
    room_type = update.callback_query.data.split(":")[1]
    context.user_data["coliving_info"].room_type = room_type
    await update.effective_message.reply_text(text=f"{templates.REPLY_MSG}{room_type}")
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_ASK_ABOUT,
        reply_markup=common_keyboards.CANCEL_KEYBOARD,
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
        min=templates.MIN_ABOUT_LENGTH,
        max=templates.MAX_ABOUT_LENGTH,
        message=templates.ERR_MSG_ABOUT_MAX_LEN.format(max=templates.MAX_ABOUT_LENGTH),
    ):
        await update.effective_message.reply_text(
            text=templates.REPLY_MSG_ASK_ABOUT,
            reply_markup=common_keyboards.CANCEL_KEYBOARD,
        )
        return states.ABOUT_ROOM

    context.user_data["coliving_info"].about = about_coliving
    await update.effective_message.reply_text(
        text=f"{templates.REPLY_MSG}{about_coliving}"
    )
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_ASK_PRICE,
        reply_markup=common_keyboards.CANCEL_KEYBOARD,
    )
    return states.PRICE


async def handle_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Ввод цены за спальное место коливинг профиля
    и сохранение в контекст.
    Перевод на state PHOTO_ROOM.
    """

    price = update.message.text
    if not await value_is_in_range_validator(
        update=update,
        context=context,
        value=price,
        min=templates.MIN_PRICE,
        max=templates.MAX_PRICE,
        message=templates.ERR_MSG_PRICE.format(
            min=templates.MIN_PRICE, max=templates.MAX_PRICE
        ),
    ):
        return states.PRICE

    context.user_data["coliving_info"].price = price
    await update.effective_message.reply_text(text=f"{templates.REPLY_MSG}{price}")
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_ASK_PHOTO_SEND,
        reply_markup=keyboards.SAVE_OR_CANCEL_PHOTO_KEYBOARD,
    )
    return states.PHOTO_ROOM


async def handle_add_or_edit_photo_room(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Обрабатывает загруженную пользователем фотографию.
    Продолжает диалог по нажатию кнопки (сохранить)
    """
    new_photo = update.effective_message.photo[-1]

    if update.message.text:
        await update.effective_message.reply_text(text=templates.ERR_PHOTO_NOT_TEXT)
        return states.EDIT_PHOTO_ROOM

    context.user_data["coliving_info"].images.append(
        Image(file_id=new_photo.file_id, photo_size=new_photo)
    )

    if len(context.user_data["coliving_info"].images) == 5:
        state = await send_edited_room_photos(update, context)
        return state
    return None


async def handle_confirm_or_cancel_profile_text_instead_of_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Подтверждение или изменение коливинг профиля.
    Проверка: ввод текста или нажатие кнопки
    """

    await update.effective_message.reply_text(
        templates.ERR_NEED_TO_SELECT_BTN,
    )
    await _show_coliving_profile(
        update,
        context,
        templates.REPLY_MSG_ASK_TO_CONFIRM,
        keyboard=keyboards.CONFIRM_OR_CANCEL_PROFILE_KEYBOARD,
    )


async def handle_profile_confirmation_cancel(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отмена редактирования коливинг профиля."""

    await update.effective_message.edit_reply_markup()
    message = templates.BTN_LABEL_CANCEL_CREATE
    await update.effective_message.reply_text(text=f"{templates.REPLY_MSG}{message}")
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_PROFILE_NO_CREATE,
    )
    context.user_data.clear()
    return ConversationHandler.END


async def handle_confirm_or_edit_reply_confirm(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Подтверждение или изменение коливинг профиля.
    Обработка ответа - подтверждение коливинг профиля.
    Перевод на установку флажка поиска IS_VISIBLE.
    """
    await update.effective_message.edit_reply_markup()
    reply = templates.BTN_LABEL_CONFIRM
    await update.effective_message.reply_text(text=f"{templates.REPLY_MSG}{reply}")
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_ASK_TO_SHOW_PROFILE,
        reply_markup=common_funcs.combine_keyboards(
            keyboards.IS_VISIBLE_OR_NOT_PROFILE_KEYBOARD,
            common_keyboards.CANCEL_KEYBOARD,
        ),
    )
    return states.IS_VISIBLE


async def repeat_question_about_coliving_visibility(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Показать или скрыть профиль в поиске.
    Проверка: ввод текста или нажатие кнопки.
    """

    await update.effective_message.reply_text(
        templates.ERR_NEED_TO_SELECT_BTN,
    )
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_ASK_TO_SHOW_PROFILE,
        reply_markup=keyboards.IS_VISIBLE_OR_NOT_PROFILE_KEYBOARD,
    )


async def handle_is_visible_coliving_profile_yes(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка ответа: показать профиль в поиске и
    перевод на стадию сохранения в БД.
    """
    await update.effective_message.edit_reply_markup()
    context.user_data["coliving_info"].is_visible = eval(update.callback_query.data)
    if context.user_data["coliving_info"].is_visible:
        respond = templates.REPLY_BTN_SHOW
    else:
        respond = templates.REPLY_BTN_HIDE
    await update.effective_message.reply_text(
        text=respond,
    )
    return await save_coliving_info_to_db(update, context)


async def handle_what_to_edit_text_instead_of_button(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Выбор редактируемого поля.
    Проверка: ввод текста или нажатие кнопки.
    """

    await update.effective_message.reply_text(text=templates.ERR_NEED_TO_SELECT_BTN)
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_WHAT_TO_EDIT,
        reply_markup=keyboards.WHAT_EDIT_PROFILE_KEYBOARD,
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
        text=f"{templates.REPLY_MSG}{templates.BTN_LABEL_FILL_AGAIN}"
    )
    context.user_data.clear()
    await update.effective_chat.send_message(
        text=templates.REPLY_MSG_ASK_LOCATION,
        reply_markup=context.bot_data["location_keyboard"],
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
        text=f"{templates.REPLY_MSG}{templates.BTN_LABEL_EDIT_LOCATION}"
    )
    await update.effective_chat.send_message(
        text=templates.REPLY_MSG_ASK_LOCATION,
        reply_markup=context.bot_data["location_keyboard"],
    )
    return states.EDIT_LOCATION


async def handle_what_to_edit_room_type(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Выбор редактируемого поля.
    Обработка ответа: Тип помещения.
    """
    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=f"{templates.REPLY_MSG}{templates.BTN_LABEL_EDIT_ROOM_TYPE}"
    )
    await update.effective_chat.send_message(
        text=templates.REPLY_MSG_ASK_ROOM_TYPE,
        reply_markup=keyboards.ROOM_TYPE_KEYBOARD,
    )
    return states.EDIT_ROOM_TYPE


async def handle_what_to_edit_about_room(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Выбор редактируемого поля.
    Обработка ответа: Описание.
    """

    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=f"{templates.REPLY_MSG}{templates.BTN_LABEL_EDIT_ABOUT_ROOM}"
    )
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_ASK_ABOUT,
    )
    return states.EDIT_ABOUT_ROOM


async def handle_what_to_edit_price(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Выбор редактируемого поля.
    Обработка ответа: Цена.
    """
    await update.effective_message.edit_reply_markup()
    await update.effective_message.reply_text(
        text=f"{templates.REPLY_MSG}{templates.BTN_LABEL_EDIT_PRICE}"
    )
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_ASK_PRICE,
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
    context.user_data["coliving_info"].images.clear()
    await update.effective_message.reply_text(
        text=f"{templates.REPLY_MSG}{templates.BTN_LABEL_EDIT_PHOTO}"
    )
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_ASK_PHOTO_SEND,
        reply_markup=keyboards.SAVE_OR_CANCEL_NEW_PHOTO_KEYBOARD,
    )
    return states.EDIT_PHOTO_ROOM


async def handle_edit_location(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Редактирование location."""

    location = update.callback_query.data.split(":")[1]
    await update.effective_message.edit_reply_markup()
    context.user_data["coliving_info"].location = location
    await update.effective_message.reply_text(text=f"{templates.REPLY_MSG}{location}")
    await _show_coliving_profile(
        update,
        context,
        templates.REPLY_MSG_ASK_TO_CONFIRM,
        keyboards.EDIT_CONFIRMATION_KEYBOARD,
    )
    return states.EDIT_CONFIRMATION


async def handle_edit_select_room_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Редактирование типа помещения."""
    room_type = update.callback_query.data.split(":")[1]
    await update.effective_message.edit_reply_markup()
    context.user_data["coliving_info"].room_type = room_type
    await update.effective_message.reply_text(text=f"{templates.REPLY_MSG}{room_type}")
    await _show_coliving_profile(
        update,
        context,
        templates.REPLY_MSG_ASK_TO_CONFIRM,
        keyboards.EDIT_CONFIRMATION_KEYBOARD,
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
        min=templates.MIN_ABOUT_LENGTH,
        max=templates.MAX_ABOUT_LENGTH,
        message=templates.ERR_MSG_ABOUT_MAX_LEN.format(max=templates.MAX_ABOUT_LENGTH),
    ):
        await update.effective_message.reply_text(
            text=templates.REPLY_MSG_ASK_ABOUT,
        )
        return states.EDIT_ABOUT_ROOM

    context.user_data["coliving_info"].about = about_coliving
    await update.effective_message.reply_text(
        text=f"{templates.REPLY_MSG}{about_coliving}"
    )
    await _show_coliving_profile(
        update,
        context,
        templates.REPLY_MSG_ASK_TO_CONFIRM,
        keyboards.EDIT_CONFIRMATION_KEYBOARD,
    )
    return states.EDIT_CONFIRMATION


async def handle_edit_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Редактирование цены коливинга."""

    edit_price = update.message.text
    if not await value_is_in_range_validator(
        update=update,
        context=context,
        value=edit_price,
        min=templates.MIN_PRICE,
        max=templates.MAX_PRICE,
        message=templates.ERR_MSG_PRICE.format(
            min=templates.MIN_PRICE, max=templates.MAX_PRICE
        ),
    ):
        return states.EDIT_PRICE

    context.user_data["coliving_info"].price = edit_price
    await update.effective_message.reply_text(text=f"{templates.REPLY_MSG}{edit_price}")
    await _show_coliving_profile(
        update,
        context,
        templates.REPLY_MSG_ASK_TO_CONFIRM,
        keyboards.EDIT_CONFIRMATION_KEYBOARD,
    )
    return states.EDIT_CONFIRMATION


async def handle_edit_profile_confirmation_text_instead_of_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Подтверждение измененного коливинг профиля.
    Продолжение редактирования. Отмена редактирования.
    Проверка: ввод текста или нажатие кнопки.
    """

    await update.effective_message.reply_text(
        templates.ERR_NEED_TO_SELECT_BTN,
    )
    await _show_coliving_profile(
        update,
        context,
        templates.REPLY_MSG_ASK_TO_CONFIRM,
        keyboards.EDIT_CONFIRMATION_KEYBOARD,
    )


async def handle_edit_profile_confirmation_confirm(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Подтверждение измененного коливинг профиля."""

    await update.effective_message.edit_reply_markup()
    message = templates.BTN_LABEL_CONFIRM
    await update.effective_message.reply_text(text=f"{templates.REPLY_MSG}{message}")
    coliving = context.user_data["coliving_info"]
    images = context.user_data["coliving_info"].images[:5]
    # Проверка наличия измененных фото по размеру первой фотографии
    if images[0].photo_size:
        await api_service.delete_coliving_photos(coliving.id, update.effective_chat.id)
        await api_service.save_coliving_photo(images, coliving)

    await api_service.update_coliving_info(coliving)
    await update.effective_message.reply_text(text=templates.REPLY_MSG_PROFILE_SAVED)
    context.user_data.clear()
    return ConversationHandler.END


async def handle_edit_profile_confirmation_cancel(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отмена редактирования коливинг профиля."""

    await update.effective_message.edit_reply_markup()
    message = templates.BTN_LABEL_CANCEL_EDIT
    await update.effective_message.reply_text(text=f"{templates.REPLY_MSG}{message}")
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_PROFILE_NO_CHANGE,
    )
    context.user_data.clear()
    ########################################
    # Куда отправить?
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_START_CREATE_PROFILE,
    )
    ########################################
    return ConversationHandler.END


async def handle_edit_profile_confirmation_continue_edit(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Продолжение редактирования коливинг профиля."""

    await update.effective_message.edit_reply_markup()
    message = templates.BTN_LABEL_EDIT_CONTINUE
    await update.effective_message.reply_text(text=f"{templates.REPLY_MSG}{message}")
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_WHAT_TO_EDIT,
        reply_markup=keyboards.WHAT_EDIT_PROFILE_KEYBOARD,
    )
    return states.EDIT


async def save_coliving_info_to_db(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Сохраняет в БД - запрос к API.
    Отправляет сообщение о завершении регистрации.
    """
    await api_service.save_coliving_info(coliving=context.user_data["coliving_info"])
    await update.effective_message.reply_text(text=templates.REPLY_MSG_PROFILE_SAVED)
    context.user_data.clear()
    return ConversationHandler.END


async def _show_coliving_profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    ask_to_confirm: bool,
    keyboard: Optional[InlineKeyboardMarkup] = None,
    coliving: Optional[Coliving] = None,
) -> None:
    """Просмотр профиля и переводит на подтверждение профиля CONFIRMATION."""
    current_chat = update.effective_chat
    coliving_info: Coliving = coliving or context.user_data["coliving_info"]

    if coliving_info.images:
        media_group = [
            InputMediaPhoto(media=image.file_id) for image in coliving_info.images[:5]
        ]
    await current_chat.send_media_group(media=media_group)

    if keyboard is None:
        if coliving_info.is_visible:
            keyboard = keyboards.COLIVING_PROFILE_KEYBOARD_VISIBLE
        else:
            keyboard = keyboards.COLIVING_PROFILE_KEYBOARD_NOT_VISIBLE

    message_text = await format_coliving_profile_message(coliving_info)

    if ask_to_confirm:
        message_text += templates.REPLY_MSG_ASK_TO_CONFIRM

    await current_chat.send_message(
        text=message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )


async def send_received_room_photos(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Сохранение фотографий
    """

    images = context.user_data["coliving_info"].images
    if len(images) > 5:
        await update.effective_message.reply_text(text=templates.ERR_PHOTO_LIMIT_TEXT)

    if images:
        await update.effective_chat.send_message(templates.REPLY_MSG_PHOTO)
        await _show_coliving_profile(
            update,
            context,
            templates.REPLY_MSG_ASK_TO_CONFIRM,
            keyboards.CONFIRM_OR_CANCEL_PROFILE_KEYBOARD,
        )
        return states.CONFIRMATION

    await context.bot.answer_callback_query(
        callback_query_id=update.callback_query.id,
        text=templates.DONT_SAVE_COLIVING_WITHOUT_PHOTO,
        show_alert=True,
    )
    return states.PHOTO_ROOM


async def send_edited_room_photos(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Подтверждение сохранения измененных фотографий
    """
    images = context.user_data["coliving_info"].images
    if len(images) > 5:
        await update.effective_message.reply_text(text=templates.ERR_PHOTO_LIMIT_TEXT)

    if images:
        await _show_coliving_profile(
            update,
            context,
            templates.REPLY_MSG_ASK_TO_CONFIRM,
            keyboards.EDIT_CONFIRMATION_KEYBOARD,
        )
        return states.EDIT_CONFIRMATION

    await context.bot.answer_callback_query(
        callback_query_id=update.callback_query.id,
        text=templates.DONT_SAVE_COLIVING_WITHOUT_PHOTO,
        show_alert=True,
    )
    return states.EDIT_PHOTO_ROOM
