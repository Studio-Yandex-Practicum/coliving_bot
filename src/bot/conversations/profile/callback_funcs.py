from copy import copy
from http import HTTPStatus as codes
from re import fullmatch
from typing import Union

from httpx import HTTPStatusError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import conversations.profile.buttons as buttons
import conversations.profile.keyboards as keyboards
import conversations.profile.templates as templates
from conversations.menu.callback_funcs import menu
from conversations.profile.states import States
from general.validators import value_is_in_range_validator
from internal_requests import api_service


async def set_profile_to_context(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    profile_info,
) -> None:
    context.user_data[templates.NAME_FIELD] = profile_info.name
    context.user_data[templates.SEX_FIELD] = profile_info.sex
    context.user_data[templates.AGE_FIELD] = profile_info.age
    context.user_data[templates.LOCATION_FIELD] = profile_info.location
    context.user_data[templates.ABOUT_FIELD] = profile_info.about
    context.user_data[templates.IS_VISIBLE_FIELD] = profile_info.is_visible
    context.user_data[templates.RECEIVED_PHOTOS_FIELD] = profile_info.images


async def start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Union[int, States]:
    """
    Начало диалога. Проверяет, не был ли пользователь зарегистрирован ранее.
    Переводит диалог в состояние AGE (ввод возраста пользователя).
    """
    try:
        profile_info = await api_service.get_user_profile_by_telegram_id(
            update.effective_chat.id
        )
    except HTTPStatusError as exc:
        if exc.response.status_code == codes.NOT_FOUND:
            await update.effective_message.edit_text(text=templates.ASK_AGE)
            return States.AGE
        raise exc
    await set_profile_to_context(update, context, profile_info)
    await update.effective_message.delete()
    await _look_at_profile(update, context, "", keyboards.PROFILE_KEYBOARD)
    return States.PROFILE


async def send_question_to_profile_is_visible_in_search(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Union[int, States]:
    """
    Обработка кнопки 'Показать в поиске'.
    Завершает диалог.
    """
    await update.effective_message.edit_reply_markup()
    is_visible: bool = eval(update.callback_query.data.split(":")[1])
    context.user_data[templates.IS_VISIBLE_FIELD] = is_visible
    if is_visible:
        message_text = templates.FORM_IS_VISIBLE
    else:
        message_text = templates.FORM_IS_NOT_VISIBLE
    await update.effective_message.reply_text(
        text=message_text, parse_mode=ParseMode.HTML
    )
    await api_service.update_user_profile(update.effective_chat.id, context.user_data)

    return ConversationHandler.END


async def send_question_to_edit_profile(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Union[int, States]:
    """
    Обработка кнопки 'Скрыть из поиска'.
    Переводит диалог в состояние EDIT.
    """
    await _send_chosen_choice_and_remove_buttons(update=update)
    await update.effective_message.reply_text(
        text=templates.ASK_WANT_TO_CHANGE,
        reply_markup=keyboards.FORM_EDIT_KEYBOARD,
    )

    return States.EDIT


async def handle_return_to_menu_response(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Union[int, States]:
    """Обработка ответа: Вернуться в меню."""

    await update.effective_message.edit_reply_markup()
    context.user_data.clear()
    await menu(update, context)
    return ConversationHandler.END


async def handle_age(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Union[int, States]:
    """
    Обрабатывает введенный пользователем возраст.
    Переводит диалог в состояние SEX (пол пользователя).
    """
    age = update.message.text
    if not await value_is_in_range_validator(
        update=update,
        context=context,
        value=age,
        min=templates.MIN_AGE,
        max=templates.MAX_AGE,
        message=templates.AGE_ERROR_MSG.format(
            min=templates.MIN_AGE, max=templates.MAX_AGE
        ),
    ):
        return States.AGE
    context.user_data[templates.AGE_FIELD] = int(age)
    await update.effective_message.reply_text(
        templates.ASK_SEX,
        reply_markup=keyboards.SEX_KEYBOARD,
    )

    return States.SEX


async def handle_sex(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Union[int, States]:
    """
    Обрабатывает введенный пользователем пол.
    Переводит диалог в состояние NAME (ввод имени пользователя).
    """
    sex = update.callback_query.data
    await update.effective_message.reply_text(text=sex)
    await update.effective_message.edit_reply_markup()
    context.user_data[templates.SEX_FIELD] = sex.split()[1].capitalize()
    await update.effective_message.reply_text(
        templates.ASK_NAME,
    )

    return States.NAME


async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает введенное пользователем имя.
    Переводит диалог в состояние LOCATION (ввод места проживания).
    """
    name = update.message.text.strip()
    if not fullmatch(templates.NAME_PATTERN, name):
        await update.effective_message.reply_text(text=templates.NAME_SYMBOL_ERROR_MSG)
        return States.NAME
    if not await value_is_in_range_validator(
        update=update,
        context=context,
        value=len(name),
        min=templates.MIN_NAME_LENGTH,
        max=templates.MAX_NAME_LENGTH,
        message=templates.NAME_LENGHT_ERROR_MSG.format(
            min=templates.MIN_NAME_LENGTH, max=templates.MAX_NAME_LENGTH
        ),
    ):
        return States.NAME
    context.user_data[templates.NAME_FIELD] = name
    await update.effective_message.reply_text(
        text=templates.ASK_LOCATION,
        reply_markup=keyboards.LOCATION_KEYBOARD,
    )

    return States.LOCATION


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает введенное пользователем желаемое место жительства.
    Переводит диалог в состояние ABOUT_YOURSELF (ввод информации о себе).
    """
    location = update.callback_query.data
    await update.effective_message.reply_text(text=location)
    await update.effective_message.edit_reply_markup()
    context.user_data[templates.LOCATION_FIELD] = location
    await update.effective_message.reply_text(
        text=templates.ASK_ABOUT,
    )

    return States.ABOUT_YOURSELF


async def handle_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает введенную пользователем информацию о себе.
    Переводит диалог в состояние PHOTO (фотография пользователя).
    """
    about = update.message.text
    if not await value_is_in_range_validator(
        update,
        context,
        len(about),
        min=templates.MIN_ABOUT_LENGTH,
        max=templates.MAX_ABOUT_LENGTH,
        message=templates.ABOUT_MAX_LEN_ERROR_MSG.format(
            max=templates.MAX_ABOUT_LENGTH
        ),
    ):
        return States.ABOUT_YOURSELF
    if context.user_data.get(templates.ABOUT_FIELD):
        context.user_data[templates.ABOUT_FIELD] = about
        await api_service.update_user_profile(
            update.effective_chat.id, context.user_data
        )
    else:
        context.user_data[templates.ABOUT_FIELD] = about
        await api_service.create_user_profile(
            update.effective_chat.id, context.user_data
        )
        context.user_data[templates.IS_VISIBLE_FIELD] = True
    await update.effective_chat.send_message(
        text=templates.ASK_PHOTO,
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(
                text=buttons.SAVE_PHOTO_BUTTON, callback_data=buttons.SAVE_PHOTO_BUTTON
            )
        ),
    ),

    return States.PHOTO


async def _look_at_profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    title: str,
    keyboard: str,
    ask: bool = False,
) -> None:
    """
    Предварительный просмотр профиля.
    """
    chat_id = update.effective_chat.id
    ask_text = copy(templates.ASK_IS_THAT_RIGHT)
    if not ask:
        ask_text = templates.ASK_WANT_TO_CHANGE
    message_text = (
        title
        + "\n"
        + templates.PROFILE_DATA.format(
            name=context.user_data.get(templates.NAME_FIELD),
            sex=context.user_data.get(templates.SEX_FIELD),
            age=context.user_data.get(templates.AGE_FIELD),
            location=context.user_data.get(templates.LOCATION_FIELD),
            about=context.user_data.get(templates.ABOUT_FIELD),
            is_visible=templates.PROFILE_IS_VISIBLE_TEXT
            if context.user_data.get(templates.IS_VISIBLE_FIELD)
            else templates.PROFILE_IS_INVISIBLE_TEXT,
        )
        + "\n"
    )
    received_photos = context.user_data.get(templates.RECEIVED_PHOTOS_FIELD, [])
    media_group = [InputMediaPhoto(file_id) for file_id in received_photos]
    await update.effective_chat.send_media_group(
        media=media_group,
        caption=message_text,
        parse_mode=ParseMode.HTML,
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=ask_text,
        reply_markup=keyboard,
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает загруженную пользователем фотографию.
    Переводит диалог в состояние CONFIRMATION (анкета верна или нет)
    """
    file_id = update.effective_message.photo[-1].file_id
    new_file = await context.bot.get_file(file_id)
    photo_bytearray = await new_file.download_as_bytearray()
    await api_service.save_photo(
        telegram_id=update.effective_chat.id,
        photo_bytearray=photo_bytearray,
        filename=new_file.file_path,
        file_id=file_id,
    )
    received_photos = context.user_data.get(templates.RECEIVED_PHOTOS_FIELD, [])
    received_photos.append(file_id)
    context.user_data[templates.RECEIVED_PHOTOS_FIELD] = received_photos

    return None


async def send_received_photos(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    if context.user_data.get(templates.RECEIVED_PHOTOS_FIELD):
        await update.effective_message.edit_reply_markup()
        await _look_at_profile(
            update,
            context,
            templates.LOOK_AT_FORM_FIRST,
            keyboards.FORM_SAVED_KEYBOARD,
            True,
        )
        return States.CONFIRMATION
    await context.bot.answer_callback_query(
        callback_query_id=update.callback_query.id,
        text=templates.DONT_SAVE_WITHOUT_PHOTO,
        show_alert=True,
    )
    return States.PHOTO


async def handle_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Выводит сообщение с заполненным профилем.
    Вызывает метод для отправки запроса на видимость анкеты,
    """
    edit = update.callback_query.data
    await update.effective_message.reply_text(text=edit)
    await update.effective_message.edit_reply_markup()
    if edit == buttons.EDIT_FORM_BUTTON:
        await update.effective_message.reply_text(
            text=templates.ASK_WANT_TO_CHANGE,
            reply_markup=keyboards.FORM_EDIT_KEYBOARD,
        )
        return States.EDIT
    elif edit == buttons.YES_BUTTON:
        await update.effective_message.reply_text(
            text=templates.ASK_FORM_VISIBLE,
            reply_markup=keyboards.FORM_VISIBLE_KEYBOARD,
        )
        return States.VISIBLE

    return States.CONFIRMATION


async def handle_visible(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Делает анкету видимой или нет.
    Переводит диалог в состояние END (сохранение анкеты).
    """
    visible = update.callback_query.data
    await update.effective_message.reply_text(text=visible)
    await update.effective_message.edit_reply_markup()
    if visible == buttons.YES_TO_DO_BUTTON:
        context.user_data[templates.IS_VISIBLE_FIELD] = True
    elif visible == buttons.HIDE_SEARCH_BUTTON:
        context.user_data[templates.IS_VISIBLE_FIELD] = False
        await api_service.update_user_profile(
            update.effective_chat.id, context.user_data
        )
    await send_confirmation_request(update, context)

    return ConversationHandler.END


async def start_filling_again(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'Заполнить заново.'.
    """
    await _send_chosen_choice_and_remove_buttons(update=update)
    await update.effective_message.reply_text(
        text=templates.ASK_AGE_AGAIN,
    )

    return States.AGE


async def send_question_to_edit_about_myself(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'О себе.'.
    """
    await _send_chosen_choice_and_remove_buttons(update=update)
    await update.effective_message.reply_text(
        text=templates.ASK_ABOUT,
    )

    return States.EDIT_ABOUT_YOURSELF


async def send_question_to_edit_photo(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'Фотографию.'.
    """
    await _send_chosen_choice_and_remove_buttons(update=update)
    await update.effective_chat.send_message(
        text=templates.ASK_NEW_PHOTO,
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(
                text=buttons.SAVE_EDITED_PHOTO_BUTTON,
                callback_data=buttons.SAVE_EDITED_PHOTO_BUTTON,
            )
        ),
    )

    return States.EDIT_PHOTO


async def _send_chosen_choice_and_remove_buttons(update: Update) -> None:
    """
    Удаление предыдущей клавиатуры.
    Спрашивает что пользователь хочет изменить.
    """
    callback_query = update.callback_query
    choice_text = callback_query.data
    await callback_query.message.edit_reply_markup()
    await callback_query.message.reply_text(text=choice_text)


async def handle_edit_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает отредактированную пользователем информацию о себе.
    Переводит диалог в состояние EDIT_CONFIRMATION (анкета верна или нет).
    """
    about = update.message.text
    if not await value_is_in_range_validator(
        update,
        context,
        len(about),
        min=templates.MIN_ABOUT_LENGTH,
        max=templates.MAX_ABOUT_LENGTH,
        message=templates.ABOUT_MAX_LEN_ERROR_MSG.format(
            max=templates.MAX_ABOUT_LENGTH
        ),
    ):
        return States.ABOUT_YOURSELF
    context.user_data[templates.ABOUT_FIELD] = about
    await _look_at_profile(
        update,
        context,
        templates.LOOK_AT_FORM_SECOND,
        keyboards.FORM_SAVE_OR_EDIT_KEYBOARD,
        True,
    )

    return States.EDIT_CONFIRMATION


async def handle_edit_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает отредактированную пользователем фотографию.
    Переводит диалог в состояние EDIT_CONFIRMATION (анкета верна или нет).
    """
    file_id = update.effective_message.photo[-1].file_id
    new_file = await context.bot.get_file(file_id)
    photo_bytearray = await new_file.download_as_bytearray()
    await api_service.save_photo(
        telegram_id=update.effective_chat.id,
        photo_bytearray=photo_bytearray,
        filename=new_file.file_path,
        file_id=file_id,
    )
    received_photos = context.user_data.get(templates.RECEIVED_PHOTOS_FIELD, [])
    received_photos.append(file_id)
    context.user_data[templates.RECEIVED_PHOTOS_FIELD] = received_photos

    return None


async def send_edited_photos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.effective_message.edit_reply_markup()
    await _look_at_profile(
        update,
        context,
        templates.LOOK_AT_FORM_THIRD,
        keyboards.FORM_SAVE_OR_EDIT_KEYBOARD,
        True,
    )

    return States.EDIT_CONFIRMATION


async def send_question_to_profile_is_correct(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Спрашивает верна ли анкета.
    Обработка кнопки 'Да. Верно'.
    Либо завершает диалог.
    """
    await _send_chosen_choice_and_remove_buttons(update=update)
    await api_service.update_user_profile(update.effective_chat.id, context.user_data)
    await send_confirmation_request(update, context)
    return ConversationHandler.END


async def send_question_to_cancel_profile_edit(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Спрашивает верна ли анкета.
    Обработка кнопки 'Отменить редактирование'.
    Либо завершает диалог.
    """
    await _send_chosen_choice_and_remove_buttons(update=update)
    await update.effective_message.reply_text(
        text=templates.FORM_NOT_CHANGED,
    )

    return ConversationHandler.END


async def send_question_to_resume_profile_edit(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Спрашивает верна ли анкета.
    Обработка кнопки 'Продолжить редактирование'.
    """
    await _send_chosen_choice_and_remove_buttons(update=update)
    await update.effective_message.reply_text(
        text=templates.ASK_WANT_TO_CHANGE,
        reply_markup=keyboards.FORM_EDIT_KEYBOARD,
    )

    return States.EDIT


async def send_confirmation_request(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Отправляет сохраняет профиль в базе данных.
    """
    await update.effective_message.reply_text(
        text=templates.FORM_SAVED,
    )
