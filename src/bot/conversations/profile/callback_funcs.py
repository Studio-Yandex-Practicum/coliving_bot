import base64
import io
from copy import copy
from re import fullmatch

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from general.validators import value_is_in_range_validator
from internal_requests import mock as api_service

from .buttons import EDIT_FORM_BUTTON, NOT_LOOK_YET_BUTTON, YES_BUTTON, YES_TO_DO_BUTTON
from .keyboards import (
    FORM_EDIT_KEYBOARD,
    FORM_SAVE_OR_EDIT_KEYBOARD,
    FORM_SAVED_KEYBOARD,
    FORM_VISIBLE_KEYBOARD,
    LOCATION_KEYBOARD,
    PROFILE_KEYBOARD,
    SEX_KEYBOARD,
)
from .states import States
from .templates import (
    ABOUT_FIELD,
    ABOUT_MAX_LEN_ERROR_MSG,
    AGE_ERROR_MSG,
    AGE_FIELD,
    ASK_ABOUT,
    ASK_AGE,
    ASK_AGE_AGAIN,
    ASK_FORM_VISIBLE,
    ASK_IS_THAT_RIGHT,
    ASK_LOCATION,
    ASK_NAME,
    ASK_NEW_PHOTO,
    ASK_PHOTO,
    ASK_SEX,
    ASK_WANT_TO_CHANGE,
    FORM_IS_NOT_VISIBLE,
    FORM_IS_VISIBLE,
    FORM_NOT_CHANGED,
    FORM_SAVED,
    IMAGE_FIELD,
    IS_VISIBLE_FIELD,
    LOCATION_FIELD,
    LOOK_AT_FORM_FIRST,
    LOOK_AT_FORM_SECOND,
    LOOK_AT_FORM_THIRD,
    MAX_ABOUT_LENGTH,
    MAX_AGE,
    MAX_NAME_LENGTH,
    MIN_ABOUT_LENGTH,
    MIN_AGE,
    MIN_NAME_LENGTH,
    NAME_FIELD,
    NAME_LENGHT_ERROR_MSG,
    NAME_PATTERN,
    NAME_SYMBOL_ERROR_MSG,
    PROFILE_DATA,
    PROFILE_IS_INVISIBLE_TEXT,
    PROFILE_IS_VISIBLE_TEXT,
    SEX_FIELD,
)


async def set_profile_to_context(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    profile_info,
) -> None:
    context.user_data[NAME_FIELD] = profile_info.name
    context.user_data[SEX_FIELD] = profile_info.sex
    context.user_data[AGE_FIELD] = profile_info.age
    context.user_data[LOCATION_FIELD] = profile_info.location
    context.user_data[ABOUT_FIELD] = profile_info.about
    context.user_data[IS_VISIBLE_FIELD] = (
        True if profile_info.is_visible == PROFILE_IS_VISIBLE_TEXT else False
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало диалога. Проверяет, не был ли пользователь зарегистрирован ранее.
    Переводит диалог в состояние AGE (ввод возраста пользователя).
    """
    flag = False  # Флаг для проверки ответвления если профиль уже заполнен
    if flag:
        profile_info = await api_service.get_user_profile_by_telegram_id(
            update.effective_chat.id
        )
        await set_profile_to_context(update, context, profile_info)
        await look_at_profile(update, context, "", PROFILE_KEYBOARD)
        return States.PROFILE
    await update.effective_message.reply_text(text=ASK_AGE)

    return States.AGE


async def send_question_to_profile_is_visible_in_search(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'Показать в поиске'.
    Завершает диалог.
    """
    await _send_chosen_choice_and_remove_buttons(update=update)
    context.user_data[IS_VISIBLE_FIELD] = True
    await update.effective_message.reply_text(
        text=FORM_IS_VISIBLE,
    )

    return ConversationHandler.END


async def send_question_to_profile_is_invisible_in_search(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'Скрыть из поиска'.
    Завершает диалог.
    """
    await _send_chosen_choice_and_remove_buttons(update=update)
    context.user_data[IS_VISIBLE_FIELD] = False
    await update.effective_message.reply_text(
        text=FORM_IS_NOT_VISIBLE,
    )

    return ConversationHandler.END


async def send_question_to_edit_profile(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'Скрыть из поиска'.
    Переводит диалог в состояние EDIT.
    """
    await _send_chosen_choice_and_remove_buttons(update=update)
    await update.effective_message.reply_text(
        text=ASK_WANT_TO_CHANGE,
        reply_markup=FORM_EDIT_KEYBOARD,
    )

    return States.EDIT


async def send_question_to_back_in_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'Вернуться'.
    Переводит диалог в состояние MENU.
    """
    await _send_chosen_choice_and_remove_buttons(update=update)

    return ConversationHandler.END  # MENU


async def handle_age(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает введенный пользователем возраст.
    Переводит диалог в состояние SEX (пол пользователя).
    """
    age = update.message.text
    if not await value_is_in_range_validator(
        update=update,
        context=context,
        value=age,
        min=MIN_AGE,
        max=MAX_AGE,
        message=AGE_ERROR_MSG.format(min=MIN_AGE, max=MAX_AGE),
    ):
        return States.AGE
    context.user_data[AGE_FIELD] = int(age)
    await update.effective_message.reply_text(
        ASK_SEX,
        reply_markup=SEX_KEYBOARD,
    )

    return States.SEX


async def handle_sex(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает введенный пользователем пол.
    Переводит диалог в состояние NAME (ввод имени пользователя).
    """
    sex = update.callback_query.data
    await update.effective_message.reply_text(text=sex)
    await update.effective_message.edit_reply_markup()
    context.user_data[SEX_FIELD] = sex.split()[1].capitalize()
    await update.effective_message.reply_text(
        ASK_NAME,
    )

    return States.NAME


async def handle_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает введенное пользователем имя.
    Переводит диалог в состояние LOCATION (ввод места проживания).
    """
    name = update.message.text.strip()
    if not fullmatch(NAME_PATTERN, name):
        await update.effective_message.reply_text(text=NAME_SYMBOL_ERROR_MSG)
        return States.NAME
    if not await value_is_in_range_validator(
        update=update,
        context=context,
        value=len(name),
        min=MIN_NAME_LENGTH,
        max=MAX_NAME_LENGTH,
        message=NAME_LENGHT_ERROR_MSG.format(
            min=MIN_NAME_LENGTH, max=MAX_NAME_LENGTH
        ),
    ):
        return States.NAME
    context.user_data[NAME_FIELD] = name
    await update.effective_message.reply_text(
        text=ASK_LOCATION,
        reply_markup=LOCATION_KEYBOARD,
    )

    return States.LOCATION


async def handle_location(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает введенное пользователем желаемое место жительства.
    Переводит диалог в состояние ABOUT_YOURSELF (ввод информации о себе).
    """
    location = update.callback_query.data
    await update.effective_message.reply_text(text=location)
    await update.effective_message.edit_reply_markup()
    context.user_data[LOCATION_FIELD] = location
    await update.effective_message.reply_text(
        text=ASK_ABOUT,
    )

    return States.ABOUT_YOURSELF


async def handle_about(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает введенную пользователем информацию о себе.
    Переводит диалог в состояние PHOTO (фотография пользователя).
    """
    about = update.message.text
    if not await value_is_in_range_validator(
        update,
        context,
        len(about),
        min=MIN_ABOUT_LENGTH,
        max=MAX_ABOUT_LENGTH,
        message=ABOUT_MAX_LEN_ERROR_MSG.format(max=MAX_ABOUT_LENGTH),
    ):
        return States.ABOUT_YOURSELF
    context.user_data[ABOUT_FIELD] = about
    await update.effective_message.reply_text(text=ASK_PHOTO)

    return States.PHOTO


async def encoding_profile_photo(
    update: Update, context: ContextTypes.DEFAULT_TYPE, photo
) -> str:
    """
    Обрабатывает загруженную пользователем фотографию.
    Возвращает ее в закодированном виде.
    """
    buffer = io.BytesIO()
    await photo.download_to_memory(buffer)
    return base64.b64encode(buffer.getvalue())


async def look_at_profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    title: str,
    keyboard: str,
    ask: bool = False,
) -> None:
    """
    Предварительный просмотр профиля.
    """
    chat_id = update._effective_chat.id
    ask_text = copy(ASK_IS_THAT_RIGHT)
    if not ask:
        ask_text = ""
    await context.bot.sendPhoto(
        chat_id=chat_id,
        photo=(
            base64.b64decode(context.user_data.get(IMAGE_FIELD))
        ),
        caption=title
        + "\n"
        + PROFILE_DATA.format(
            name=context.user_data.get(NAME_FIELD),
            sex=context.user_data.get(SEX_FIELD),
            age=context.user_data.get(AGE_FIELD),
            location=context.user_data.get(LOCATION_FIELD),
            about=context.user_data.get(ABOUT_FIELD),
            is_visible=PROFILE_IS_VISIBLE_TEXT
            if context.user_data.get(IS_VISIBLE_FIELD)
            else PROFILE_IS_INVISIBLE_TEXT,
        )
        + "\n"
        + ask_text,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )


async def handle_photo(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает загруженную пользователем фотографию.
    Переводит диалог в состояние CONFIRMATION (анкета верна или нет)
    """
    context.user_data[IMAGE_FIELD] = await encoding_profile_photo(
        update, context, await update.message.photo[-1].get_file()
    )
    await look_at_profile(
        update, context, LOOK_AT_FORM_FIRST, FORM_SAVED_KEYBOARD, True
    )

    return States.CONFIRMATION


async def handle_profile(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Выводит сообщение с заполненным профилем.
    Вызывает метод для отправки запроса на видимость анкеты,
    """
    edit = update.callback_query.data
    await update.effective_message.reply_text(text=edit)
    await update.effective_message.edit_reply_markup()
    if edit == EDIT_FORM_BUTTON:
        await update.effective_message.reply_text(
            text=ASK_WANT_TO_CHANGE,
            reply_markup=FORM_EDIT_KEYBOARD,
        )
        return States.EDIT
    elif edit == YES_BUTTON:
        await update.effective_message.reply_text(
            text=ASK_FORM_VISIBLE,
            reply_markup=FORM_VISIBLE_KEYBOARD,
        )
        return States.VISIBLE

    return States.CONFIRMATION


async def handle_visible(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Делает анкету видимой или нет.
    Переводит диалог в состояние END (сохранение анкеты).
    """
    visible = update.callback_query.data
    await update.effective_message.reply_text(text=visible)
    await update.effective_message.edit_reply_markup()
    if visible == YES_TO_DO_BUTTON:
        context.user_data[IS_VISIBLE_FIELD] = True
    elif visible == NOT_LOOK_YET_BUTTON:
        context.user_data[IS_VISIBLE_FIELD] = False
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
        text=ASK_AGE_AGAIN,
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
        text=ASK_ABOUT,
    )

    return States.EDIT_ABOUT_YOURSELF


async def send_question_to_edit_photo(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'Фотографию.'.
    """
    await _send_chosen_choice_and_remove_buttons(update=update)
    await update.effective_message.reply_text(
        text=ASK_NEW_PHOTO,
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


async def handle_edit_about(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает отредактированную пользователем информацию о себе.
    Переводит диалог в состояние EDIT_CONFIRMATION (анкета верна или нет).
    """
    about = update.message.text
    if not await value_is_in_range_validator(
        update,
        context,
        len(about),
        min=MIN_ABOUT_LENGTH,
        max=MAX_ABOUT_LENGTH,
        message=ABOUT_MAX_LEN_ERROR_MSG.format(max=MAX_ABOUT_LENGTH),
    ):
        return States.ABOUT_YOURSELF
    context.user_data[ABOUT_FIELD] = about
    await look_at_profile(
        update,
        context,
        LOOK_AT_FORM_SECOND,
        FORM_SAVE_OR_EDIT_KEYBOARD,
        True,
    )

    return States.EDIT_CONFIRMATION


async def handle_edit_photo(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает отредактированную пользователем фотографию.
    Переводит диалог в состояние EDIT_CONFIRMATION (анкета верна или нет).
    """
    context.user_data[IMAGE_FIELD] = await encoding_profile_photo(
        update, context, await update.message.photo[-1].get_file()
    )
    await look_at_profile(
        update,
        context,
        LOOK_AT_FORM_THIRD,
        FORM_SAVE_OR_EDIT_KEYBOARD,
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
        text=FORM_NOT_CHANGED,
    )
    await send_confirmation_request(update, context)

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
        text=ASK_WANT_TO_CHANGE,
        reply_markup=FORM_EDIT_KEYBOARD,
    )

    return States.EDIT


async def send_confirmation_request(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Отправляет сохраняет профиль в базе данных.
    """
    # save to database
    await update.effective_message.reply_text(
        text=FORM_SAVED,
    )
