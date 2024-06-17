from typing import Optional, Union

from httpx import HTTPStatusError, codes
from telegram import InlineKeyboardMarkup, InputMediaPhoto, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ContextTypes, ConversationHandler

import conversations.common_functions.common_funcs as common_funcs
import conversations.common_functions.common_templates as common_templates
import conversations.profile.constants as consts
import conversations.profile.keyboards as keyboards
import conversations.profile.templates as templates
from conversations.common_functions.common_funcs import add_response_prefix
from conversations.profile.states import States
from general.validators import value_is_in_range_validator
from internal_requests import api_service
from internal_requests.entities import Image, UserProfile


async def start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Union[int, States]:
    """
    Начало диалога. Проверяет, не был ли пользователь зарегистрирован ранее.
    Переводит диалог в состояние AGE (ввод возраста пользователя).
    """
    try:
        context.user_data["profile_info"] = (
            await api_service.get_user_profile_by_telegram_id(update.effective_chat.id)
        )
    except HTTPStatusError as exc:
        if exc.response.status_code == codes.NOT_FOUND:
            await update.effective_message.edit_text(text=templates.ASK_NAME)
            return States.NAME
        raise exc

    await update.effective_message.delete()

    keyboard = (
        keyboards.VISIBLE_PROFILE_KEYBOARD
        if context.user_data["profile_info"].is_visible
        else keyboards.HIDDEN_PROFILE_KEYBOARD
    )
    await _look_at_profile(update, context, "", keyboard)

    return States.PROFILE


@add_response_prefix()
async def send_question_to_profile_is_visible_in_search(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'Показать в поиске'.
    Завершает диалог.
    """
    visibility_choice: bool = await common_funcs.get_visibility_choice(update=update)

    message_text = common_templates.VISIBILITY_MSG_OPTNS[visibility_choice]

    context.user_data["profile_info"].is_visible = visibility_choice

    context.user_data["profile_info"] = await api_service.update_user_profile(
        context.user_data["profile_info"]
    )

    keyboard = (
        keyboards.VISIBLE_PROFILE_KEYBOARD
        if context.user_data["profile_info"].is_visible
        else keyboards.HIDDEN_PROFILE_KEYBOARD
    )
    await _look_at_profile(update, context, message_text, keyboard)

    return States.PROFILE


@add_response_prefix()
async def send_question_to_edit_profile(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> Union[int, States]:
    """
    Обработка кнопки 'Изменить анкету'.
    Переводит диалог в состояние EDIT.
    """
    await update.effective_message.reply_text(
        text=templates.ASK_WANT_TO_CHANGE,
        reply_markup=keyboards.FORM_EDIT_KEYBOARD,
    )

    return States.EDIT


@add_response_prefix()
async def handle_return_to_profile_response(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Union[int, States]:
    """
    Обработка кнопки 'Вернуться'.
    Переводит диалог в состояние PROFILE.
    """
    if context.user_data["profile_info"].is_visible is True:
        await _look_at_profile(update, context, "", keyboards.VISIBLE_PROFILE_KEYBOARD)
    else:
        await _look_at_profile(update, context, "", keyboards.HIDDEN_PROFILE_KEYBOARD)
    return States.PROFILE


async def handle_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Optional[int]:
    """
    Обрабатывает введенное пользователем имя.
    Переводит диалог в состояние AGE (ввод возраста).
    """
    name = update.effective_message.text
    if not await value_is_in_range_validator(
        update=update,
        context=context,
        value=len(name),
        min=consts.MIN_NAME_LENGTH,
        max=consts.MAX_NAME_LENGTH,
        message=templates.NAME_LENGTH_ERROR_MSG.format(
            min=consts.MIN_NAME_LENGTH, max=consts.MAX_NAME_LENGTH
        ),
    ):
        return None
    context.user_data["profile_info"] = UserProfile(
        user=update.effective_chat.id, name=name
    )
    await update.effective_message.reply_text(
        text=templates.ASK_AGE,
    )

    return States.AGE


async def handle_wrong_name(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.effective_chat.send_message(text=templates.NAME_SYMBOL_ERROR_MSG)
    return None


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
        min=consts.MIN_AGE,
        max=consts.MAX_AGE,
        message=templates.AGE_ERROR_MSG,
    ):
        return States.AGE

    context.user_data["profile_info"].age = int(age)
    await update.effective_message.reply_text(
        templates.ASK_SEX, reply_markup=keyboards.SEX_KEYBOARD
    )

    return States.SEX


async def handle_wrong_age(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_message(templates.AGE_ERROR_MSG)
    return None


@add_response_prefix()
async def handle_sex(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Union[int, States]:
    """
    Обрабатывает введенный пользователем пол.
    Переводит диалог в состояние LOCATION (ввод места пользователя).
    """
    await _save_response_about_sex(update, context)
    await update.effective_message.reply_text(
        templates.ASK_LOCATION,
        reply_markup=context.bot_data["location_keyboard"],
    )

    return States.LOCATION


@add_response_prefix()
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает введенное пользователем желаемое место жительства.
    Переводит диалог в состояние ABOUT_YOURSELF (ввод информации о себе).
    """
    await _save_response_about_location(update, context)
    await update.effective_message.reply_text(text=templates.ASK_ABOUT)

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
        min=consts.MIN_ABOUT_LENGTH,
        max=consts.MAX_ABOUT_LENGTH,
        message=templates.ABOUT_MAX_LEN_ERROR_MSG.format(max=consts.MAX_ABOUT_LENGTH),
    ):
        return States.ABOUT_YOURSELF
    context.user_data["profile_info"].about = about
    await update.effective_chat.send_message(
        text=templates.ASK_PHOTO, reply_markup=keyboards.PHOTO_KEYBOARD
    )

    return States.PHOTO


async def _look_at_profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    title: str,
    keyboard: Optional[InlineKeyboardMarkup] = None,
    ask_text: str = templates.PROFILE_VIEWING,
) -> None:
    """
    Предварительный просмотр профиля.
    """
    if title:
        await update.effective_chat.send_message(text=title)
    message_text = templates.PROFILE_DATA.format(
        name=context.user_data["profile_info"].name,
        sex=context.user_data["profile_info"].sex,
        age=context.user_data["profile_info"].age,
        location=context.user_data["profile_info"].location,
        about=context.user_data["profile_info"].about,
        is_visible=(
            common_templates.PROFILE_IS_VISIBLE_TEXT
            if context.user_data["profile_info"].is_visible
            else common_templates.PROFILE_IS_HIDDEN_TEXT
        ),
    )
    images = context.user_data["profile_info"].images
    if images:
        media_group = [InputMediaPhoto(file.file_id) for file in images]
        await update.effective_chat.send_media_group(
            media=media_group,
            caption=message_text,
        )
    else:
        await update.effective_chat.send_message(text=message_text)

    if ask_text and keyboard is not None:
        await update.effective_chat.send_message(text=ask_text, reply_markup=keyboard)


async def handle_photo(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Optional[int]:
    """
    Обрабатывает загруженную пользователем фотографию.
    Переводит диалог в состояние CONFIRMATION (анкета верна или нет)
    """

    new_photo = update.effective_message.photo[-1]

    context.user_data["profile_info"].images.append(
        Image(file_id=new_photo.file_id, photo_size=new_photo)
    )

    if len(context.user_data["profile_info"].images) == templates.PHOTO_MAX_NUMBER:
        state = await send_received_photos(update, context)
        return state

    return None


async def handle_edit_photo(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Optional[int]:
    """
    Обрабатывает загруженную пользователем фотографию.
    Переводит диалог в состояние CONFIRMATION (анкета верна или нет)
    """
    new_photo = update.effective_message.photo[-1]
    context.user_data["profile_info"].images.append(
        Image(file_id=new_photo.file_id, photo_size=new_photo)
    )

    if len(context.user_data["profile_info"].images) == templates.PHOTO_MAX_NUMBER:
        state = await send_edited_photos(update, context)
        return state

    return None


async def send_received_photos(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Optional[int]:
    images = context.user_data["profile_info"].images
    if images:
        await update.effective_message.reply_text(
            text=templates.LOOK_AT_FORM_FIRST,
            reply_markup=ReplyKeyboardRemove(),
        )
        await _look_at_profile(
            update,
            context,
            "",
            keyboards.FORM_SAVED_KEYBOARD,
            templates.ASK_IS_THAT_RIGHT,
        )
        return States.CONFIRMATION
    await update.effective_message.reply_text(text=templates.DONT_SAVE_WITHOUT_PHOTO)
    return None


@add_response_prefix()
async def handle_profile_cancel_confirmation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отмена создания профиля."""
    await update.effective_message.reply_text(
        text=templates.CANCEL_PROFILE_CREATION,
    )
    context.user_data.clear()

    return ConversationHandler.END


@add_response_prefix()
async def handle_ok_to_save(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик кнопки Да, все верно.
    Переводит в состояние VISIBLE.
    """
    await update.effective_message.reply_text(
        text=templates.ASK_FORM_VISIBLE,
        reply_markup=keyboards.FORM_VISIBLE_KEYBOARD,
    )
    return States.VISIBLE


@add_response_prefix()
async def handle_visible(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Делает анкету видимой или нет.
    Переводит диалог в состояние END (сохранение анкеты).
    """
    visibility_choice: bool = await common_funcs.get_visibility_choice(update=update)

    context.user_data["profile_info"].is_visible = visibility_choice

    await api_service.create_user_profile(context.user_data["profile_info"])
    await send_profile_saved_notification(update, context)

    return ConversationHandler.END


@add_response_prefix()
async def handle_delete_profile(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Выбор р.
    Обработка ответа: Удалить анкету.
    """
    telegram_id = update.effective_chat.id
    residence_check = await api_service.get_user_profile_by_telegram_id(telegram_id)
    if residence_check.residence is not None or residence_check.has_coliving is True:
        await update.callback_query.answer(
            text=templates.CANNOT_BE_DELETED, show_alert=True
        )
        await update.effective_message.reply_text(text=templates.DELETE_CANCELED)
        return ConversationHandler.END
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_WANT_TO_DELETE,
        reply_markup=keyboards.DELETE_OR_CANCEL_PROFILE_KEYBOARD,
    )
    return States.DELETE_PROFILE


@add_response_prefix()
async def handle_delete_profile_confirmation_confirm(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Подтверждение и удаление анкеты.
    """
    await api_service.delete_profile(telegram_id=update.effective_chat.id)
    context.user_data.clear()
    await update.effective_message.reply_text(text=templates.REPLY_MSG_PROFILE_DELETED)

    return ConversationHandler.END


@add_response_prefix()
async def handle_delete_profile_confirmation_cancel(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Отмена удаления анкеты.
    """
    context.user_data.clear()
    await update.effective_message.reply_text(
        text=templates.REPLY_MSG_PROFILE_NO_CHANGE
    )
    return ConversationHandler.END


@add_response_prefix()
async def handle_profile_confirmation_cancel(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отмена редактирования профиля."""
    await update.effective_message.reply_text(
        text=templates.CANCEL_PROFILE_CREATION,
    )
    context.user_data.clear()

    return ConversationHandler.END


@add_response_prefix()
async def send_question_to_edit_name(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'Имя'.
    """
    await update.effective_message.reply_text(
        text=templates.ASK_NAME_AGAIN,
    )

    return States.EDIT_NAME


@add_response_prefix()
async def send_question_to_edit_sex(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'Пол'.
    """
    await update.effective_message.reply_text(
        text=templates.ASK_SEX,
        reply_markup=keyboards.SEX_KEYBOARD,
    )

    return States.EDIT_SEX


@add_response_prefix()
async def send_question_to_edit_age(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'Возраст'.
    """
    await update.effective_message.reply_text(
        text=templates.ASK_AGE,
    )

    return States.EDIT_AGE


@add_response_prefix()
async def send_question_to_edit_location(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'Место проживания'.
    """
    await update.effective_message.reply_text(
        text=templates.ASK_LOCATION, reply_markup=context.bot_data["location_keyboard"]
    )

    return States.EDIT_LOCATION


@add_response_prefix()
async def send_question_to_edit_about_myself(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'О себе.'.
    """
    await update.effective_message.reply_text(
        text=templates.ASK_ABOUT,
    )

    return States.EDIT_ABOUT_YOURSELF


@add_response_prefix()
async def send_question_to_edit_photo(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'Фотографию.'.
    """
    context.user_data["profile_info"].images.clear()
    await update.effective_chat.send_message(
        text=templates.ASK_PHOTO, reply_markup=keyboards.PHOTO_EDIT_KEYBOARD
    )
    return States.EDIT_PHOTO


async def handle_edit_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Optional[int]:
    """
    Обрабатывает отредактированное пользователем имя.
    Переводит диалог в состояние EDIT_CONFIRMATION (анкета верна или нет).
    """
    name = update.effective_message.text
    if not await value_is_in_range_validator(
        update=update,
        context=context,
        value=len(name),
        min=consts.MIN_NAME_LENGTH,
        max=consts.MAX_NAME_LENGTH,
        message=templates.NAME_LENGTH_ERROR_MSG.format(
            min=consts.MIN_NAME_LENGTH, max=consts.MAX_NAME_LENGTH
        ),
    ):
        return None
    context.user_data["profile_info"].name = name
    await _look_at_profile(
        update,
        context,
        templates.LOOK_AT_FORM_SECOND,
        keyboards.FORM_SAVE_OR_EDIT_KEYBOARD,
        templates.ASK_IS_THAT_RIGHT,
    )

    return States.EDIT_CONFIRMATION


@add_response_prefix()
async def handle_edit_sex(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает отредактированную информацию касательно пола.
    Переводит диалог в состояние EDIT_CONFIRMATION (анкета верна или нет).
    """
    await _save_response_about_sex(update, context)
    await _look_at_profile(
        update,
        context,
        templates.LOOK_AT_FORM_SECOND,
        keyboards.FORM_SAVE_OR_EDIT_KEYBOARD,
        templates.ASK_IS_THAT_RIGHT,
    )

    return States.EDIT_CONFIRMATION


async def handle_edit_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает отредактированный возраст.
    Переводит диалог в состояние EDIT_CONFIRMATION (анкета верна или нет).
    """
    context.user_data["profile_info"].age = int(update.message.text)
    await _look_at_profile(
        update,
        context,
        templates.LOOK_AT_FORM_SECOND,
        keyboards.FORM_SAVE_OR_EDIT_KEYBOARD,
        templates.ASK_IS_THAT_RIGHT,
    )

    return States.EDIT_CONFIRMATION


@add_response_prefix()
async def handle_edit_location(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обрабатывает отредактированный город.
    Переводит диалог в состояние EDIT_CONFIRMATION (анкета верна или нет).
    """
    await _save_response_about_location(update, context)
    await _look_at_profile(
        update,
        context,
        templates.LOOK_AT_FORM_SECOND,
        keyboards.FORM_SAVE_OR_EDIT_KEYBOARD,
        templates.ASK_IS_THAT_RIGHT,
    )

    return States.EDIT_CONFIRMATION


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
        min=consts.MIN_ABOUT_LENGTH,
        max=consts.MAX_ABOUT_LENGTH,
        message=templates.ABOUT_MAX_LEN_ERROR_MSG.format(max=consts.MAX_ABOUT_LENGTH),
    ):
        return States.EDIT_ABOUT_YOURSELF
    context.user_data["profile_info"].about = about
    await _look_at_profile(
        update,
        context,
        templates.LOOK_AT_FORM_SECOND,
        keyboards.FORM_SAVE_OR_EDIT_KEYBOARD,
        templates.ASK_IS_THAT_RIGHT,
    )

    return States.EDIT_CONFIRMATION


async def send_edited_photos(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Optional[int]:
    images = context.user_data["profile_info"].images
    if images:
        await update.effective_message.reply_text(
            text=templates.LOOK_AT_FORM_THIRD,
            reply_markup=ReplyKeyboardRemove(),
        )
        await _look_at_profile(
            update,
            context,
            "",
            keyboards.FORM_SAVE_OR_EDIT_KEYBOARD,
            templates.ASK_IS_THAT_RIGHT,
        )
        return States.EDIT_CONFIRMATION
    await update.effective_message.reply_text(
        text=templates.DONT_SAVE_WITHOUT_PHOTO,
    )
    return None


@add_response_prefix()
async def handle_ok_to_correctness_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Обработка кнопки 'Да. Верно'.
    Либо завершает диалог.
    """
    profile = context.user_data["profile_info"]
    images = profile.images[: consts.PHOTO_MAX_NUMBER]
    if images and images[0].photo_size:
        await api_service.delete_profile_photos(update.effective_chat.id)
        await api_service.save_profile_photo(images, profile)
    await api_service.update_user_profile(profile)
    await send_profile_saved_notification(update, context)
    context.user_data.clear()
    return ConversationHandler.END


@add_response_prefix()
async def send_question_to_cancel_profile_edit(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Спрашивает верна ли анкета.
    Обработка кнопки 'Отменить редактирование'.
    Либо завершает диалог.
    """
    await update.effective_message.reply_text(
        text=templates.FORM_NOT_CHANGED,
    )

    return ConversationHandler.END


@add_response_prefix()
async def send_question_to_resume_profile_edit(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Спрашивает верна ли анкета.
    Обработка кнопки 'Продолжить редактирование'.
    """
    await update.effective_message.reply_text(
        text=templates.ASK_WANT_TO_CHANGE,
        reply_markup=keyboards.FORM_EDIT_KEYBOARD,
    )

    return States.EDIT


async def send_profile_saved_notification(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Отправляет сообщение о том, что профиль сохранён в БД.
    """
    await update.effective_message.reply_text(
        text=templates.FORM_SAVED,
    )


async def _save_response_about_sex(update: Update, context: CallbackContext):
    """Сохраняет полученный ответ про пол пользователя в контекст."""
    sex = update.callback_query.data
    context.user_data["profile_info"].sex = sex.split()[1].capitalize()


async def _save_response_about_location(update, context):
    location = update.callback_query.data.split(":")[1]
    context.user_data["profile_info"].location = location
