import base64
from copy import copy
from pathlib import Path
from re import fullmatch

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from internal_requests import mock as api_service

from .buttons import (
    ABOUT_BUTTON,
    BACK_BUTTON,
    EDIT_CANCEL_BUTTON,
    EDIT_FORM_BUTTON,
    EDIT_RESUME_BUTTON,
    FILL_AGAIN_BUTTON,
    HIDE_SEARCH_BUTTON,
    NEW_PHOTO_BUTTON,
    NOT_LOOK_YET_BUTTON,
    SHOW_SEARCH_BUTTON,
    YES_BUTTON,
    YES_TO_DO_BUTTON,
)
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
from .template import (
    ABOUT_FIELD,
    ABOUT_MAX_LEN_ERROR_MSG,
    AGE_FIELD,
    AGE_LENGHT_ERROR_MSG,
    AGE_TYPE_ERROR_MSG,
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
    BUTTON_ERROR_MSG,
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
    MIN_AGE,
    MIN_NAME_LENGTH,
    NAME_FIELD,
    NAME_LENGHT_ERROR_MSG,
    NAME_PATTERN,
    NAME_SYMBOL_ERROR_MSG,
    PHOTO_ERROR_MESSAGE,
    PROFILE_DATA,
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
    context.user_data[IS_VISIBLE_FIELD] = profile_info.is_visible


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало диалога. Проверяет, не был ли пользователь зарегистрирован ранее.
    Переводит диалог в состояние AGE (ввод возраста пользователя).
    """
    flag = False
    if flag:
        profile_info = await api_service.get_user_profile_by_telegram_id(
            update.effective_chat.id
        )
        await set_profile_to_context(update, context, profile_info)
        await look_at_profile(update, context, '', PROFILE_KEYBOARD)
        return States.PROFILE
    await update.effective_message.reply_text(text=ASK_AGE)
    return States.AGE


async def handle_fill_profile(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Показывает пользовательскую анкету.
    Переводит диалог в состояние EDIT(редактирование).
    """
    try:
        callback = update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(
            BUTTON_ERROR_MSG,
        )
        return States.PROFILE
    await update.effective_message.reply_text(text=callback)
    await update.effective_message.edit_reply_markup()
    if callback == SHOW_SEARCH_BUTTON:
        context.user_data[IS_VISIBLE_FIELD] = True
        await update.effective_message.reply_text(
            FORM_IS_VISIBLE,
        )
        return ConversationHandler.END
    elif callback == HIDE_SEARCH_BUTTON:
        context.user_data[IS_VISIBLE_FIELD] = False
        await update.effective_message.reply_text(
            FORM_IS_NOT_VISIBLE,
        )
        return ConversationHandler.END
    elif callback == EDIT_FORM_BUTTON:
        await update.effective_message.reply_text(
            ASK_WANT_TO_CHANGE,
            reply_markup=FORM_EDIT_KEYBOARD,
        )
        return States.EDIT
    elif callback == BACK_BUTTON:
        return ConversationHandler.END  # States.MENU

    return States.PROFILE


async def handle_age(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает введенный пользователем возраст.
    Переводит диалог в состояние SEX (пол пользователя).
    """
    try:
        age = int(update.message.text)
    except ValueError:
        await update.effective_message.reply_text(AGE_TYPE_ERROR_MSG)
        return States.AGE
    if age < MIN_AGE or age > MAX_AGE:
        await update.effective_message.reply_text(
            AGE_LENGHT_ERROR_MSG.format(
                min=MIN_AGE, max=MAX_AGE
            )
        )
        return States.AGE
    context.user_data[AGE_FIELD] = age
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
    try:
        sex = update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(
            BUTTON_ERROR_MSG,
        )
        return States.SEX
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
        await update.effective_message.reply_text(
            text=NAME_SYMBOL_ERROR_MSG
        )
        return States.NAME
    if (
        len(name) < MIN_NAME_LENGTH
        or len(name) > MAX_NAME_LENGTH
    ):
        await update.effective_message.reply_text(
            text=NAME_LENGHT_ERROR_MSG.format(
                min=MIN_NAME_LENGTH, max=MAX_NAME_LENGTH
            )
        )
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
    try:
        location = update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(
            BUTTON_ERROR_MSG,
        )
        return States.LOCATION
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
    if len(about) > MAX_ABOUT_LENGTH:
        await update.effective_message.reply_text(
            text=ABOUT_MAX_LEN_ERROR_MSG.format(
                max=MAX_ABOUT_LENGTH
            )
        )
        return States.ABOUT_YOURSELF
    context.user_data[ABOUT_FIELD] = about
    await update.effective_message.reply_text(text=ASK_PHOTO)

    return States.PHOTO


async def encoding_profile_photo(
    update: Update, context: ContextTypes.DEFAULT_TYPE, photo
) -> str:
    user = update.message.from_user
    path = f'files/{update._effective_chat.id}/photos'
    Path(path).mkdir(parents=True, exist_ok=True)
    await photo.download_to_drive(f'{path}/{user.full_name}_photo.jpg')
    with open(f'{path}/{user.full_name}_photo.jpg', 'rb') as image:
        return base64.b64encode(image.read())


async def look_at_profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    title: str,
    keyboard: str,
    ask: bool = False,
) -> None:
    chat_id = update._effective_chat.id
    ask_text = copy(ASK_IS_THAT_RIGHT)
    if not ask:
        ask_text = ''
    await context.bot.sendPhoto(
        chat_id=chat_id,
        photo=(
            f'files/{chat_id}/photos/{update.message.from_user.full_name}_photo.jpg'
        ),
        caption=title
        + '\n'
        + PROFILE_DATA.format(
            name=context.user_data.get(NAME_FIELD),
            sex=context.user_data.get(SEX_FIELD),
            age=context.user_data.get(AGE_FIELD),
            location=context.user_data.get(LOCATION_FIELD),
            about=context.user_data.get(ABOUT_FIELD),
            is_visible=False,
        )
        + '\n'
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
    if update.message.text:
        await update.effective_message.reply_text(
            text=PHOTO_ERROR_MESSAGE
        )
        return States.PHOTO
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
    try:
        edit = update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(
            BUTTON_ERROR_MSG,
        )
        return States.CONFIRMATION
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
    try:
        visible = update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(
            BUTTON_ERROR_MSG,
        )
        return States.VISIBLE
    await update.effective_message.reply_text(text=visible)
    await update.effective_message.edit_reply_markup()
    if visible == YES_TO_DO_BUTTON:
        context.user_data[IS_VISIBLE_FIELD] = True
    elif visible == NOT_LOOK_YET_BUTTON:
        context.user_data[IS_VISIBLE_FIELD] = False
    await send_confirmation_request(update, context)

    return ConversationHandler.END


async def handle_edit(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Спрашивает какие поля анкеты изменить.
    Переводит диалог в состояние AGE(возраст).
    """
    try:
        edit = update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(
            BUTTON_ERROR_MSG,
        )
        return States.EDIT
    await update.effective_message.reply_text(text=edit)
    await update.effective_message.edit_reply_markup()
    if edit == FILL_AGAIN_BUTTON:
        await update.effective_message.reply_text(
            text=ASK_AGE_AGAIN,
        )
        return States.AGE
    elif edit == ABOUT_BUTTON:
        await update.effective_message.reply_text(
            text=ASK_ABOUT,
        )
        return States.EDIT_ABOUT_YOURSELF
    elif edit == NEW_PHOTO_BUTTON:
        await update.effective_message.reply_text(
            text=ASK_NEW_PHOTO,
        )
        return States.EDIT_PHOTO

    return States.EDIT


async def handle_edit_about(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает отредактированную пользователем информацию о себе.
    Переводит диалог в состояние EDIT_CONFIRMATION (анкета верна или нет).
    """
    about = update.message.text
    if len(about) > MAX_ABOUT_LENGTH:
        await update.effective_message.reply_text(
            text=ABOUT_MAX_LEN_ERROR_MSG
        )
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
    if update.message.text:
        await update.effective_message.reply_text(
            text=PHOTO_ERROR_MESSAGE
        )
        return States.EDIT_PHOTO
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


async def handle_edit_confirmation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Спрашивает верна ли анкета.
    Переводит диалог в состояние EDIT(редактирование).
    Либо завершает диалог.
    """
    try:
        edit = update.callback_query.data
    except AttributeError:
        await update.effective_message.reply_text(
            BUTTON_ERROR_MSG,
        )
        return States.EDIT_CONFIRMATION
    await update.effective_message.reply_text(text=edit)
    await update.effective_message.edit_reply_markup()
    if edit == YES_BUTTON:
        await send_confirmation_request(update, context)
        return ConversationHandler.END
    elif edit == EDIT_CANCEL_BUTTON:
        await update.effective_message.reply_text(
            text=FORM_NOT_CHANGED,
        )
        await send_confirmation_request(update, context)
        return ConversationHandler.END
    elif edit == EDIT_RESUME_BUTTON:
        await update.effective_message.reply_text(
            text=ASK_WANT_TO_CHANGE,
            reply_markup=FORM_EDIT_KEYBOARD,
        )
        return States.EDIT

    return States.EDIT_CONFIRMATION


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
