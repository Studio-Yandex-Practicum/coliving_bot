from typing import Dict, Union

from telegram import InputMediaPhoto, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from conversations.complain import states
from conversations.complain.keyboards import (
    SCREENSHOT_KEYBOARD,
    get_category_keyboard,
    get_report_or_not_keyboard,
    get_screenshot_or_not_keyboard,
)
from conversations.complain.templates import (
    ASK_COMPLAIN_TEXT,
    ASK_SCREENSHOT,
    CATEGORY_CHOOSE_TEXT,
    COMPLAIN_ERROR_TEXT,
    COMPLAIN_TEXT,
    REPORT_DATA,
    SCREENSHOT_ATTACH_TEXT,
)
from internal_requests.entities import Categories, Image, Report


async def complain(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """
    Начало жалобы, проверяет - осуществляется ли просмотр анкеты.
    """
    await update.effective_message.reply_text(
        text="Сформировать жалобу",
        reply_markup=ReplyKeyboardRemove(),
    )
    if len(_context.user_data) == 0:
        await update.effective_chat.send_message(
            text=COMPLAIN_ERROR_TEXT,
        )
        return ConversationHandler.END
    await _clear_complain_info_context(_context)
    reported_user_dict = await _get_reported_user_id_and_user_id(_context)
    await agree_or_not(update=update, reported_user_dict=reported_user_dict)
    _context.user_data["complain_info"] = Report(
        reported_user=reported_user_dict["reported_user_id"],
        reporter=update.effective_chat.id,
        text="",
        category=Categories.CATEGORY_OTHER,
    )
    return ConversationHandler.END


async def agree_or_not(update: Update, reported_user_dict: Dict[str, Union[int, str]]):
    report_or_not_keyboard = await get_report_or_not_keyboard(
        reported_user_dict["reported_user_id"]
    )
    await update.effective_chat.send_message(
        text=COMPLAIN_TEXT + reported_user_dict["reported_user_name"] + "?",
        reply_markup=report_or_not_keyboard,
    )


async def category_choose(
    update: Update,
    _context: ContextTypes.DEFAULT_TYPE,
):
    category_keyboard = await get_category_keyboard()
    await update.effective_message.edit_text(
        text=CATEGORY_CHOOSE_TEXT,
        reply_markup=category_keyboard,
    )
    return states.CATEGORY


async def handle_category(
    update: Update,
    _context: ContextTypes.DEFAULT_TYPE,
):
    await update.effective_message.edit_text(
        text=ASK_COMPLAIN_TEXT,
    )
    return states.COMPLAIN_TEXT


async def handle_complain_text(
    update: Update,
    _context: ContextTypes.DEFAULT_TYPE,
):
    text = update.message.text
    _context.user_data["complain_info"].text = text
    screenshot_keyboard = await get_screenshot_or_not_keyboard()
    await update.effective_message.reply_text(
        text=SCREENSHOT_ATTACH_TEXT,
        reply_markup=screenshot_keyboard,
    )
    return states.SCREENSHOT


async def attach_screenshot(
    update: Update,
    _context: ContextTypes.DEFAULT_TYPE,
):
    await update.effective_message.reply_text(
        text="Отлично, скриншот поможет установить нарушение!",
        reply_markup=ReplyKeyboardRemove(),
    )
    await update.effective_chat.send_message(
        text=ASK_SCREENSHOT, reply_markup=SCREENSHOT_KEYBOARD
    )


async def handle_screenshot(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    new_screenshot = update.effective_message.photo[-1]
    _context.user_data["complain_info"].screenshot.append(
        Image(file_id=new_screenshot.file_id, photo_size=new_screenshot)
    )
    return states.RESULT


async def final_report(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    message_text = REPORT_DATA.format(
        user_id=_context.user_data["complain_info"].reported_user,
        category=_context.user_data["complain_info"].category.value,
        text=_context.user_data["complain_info"].text,
    )
    images = _context.user_data["complain_info"].screenshot
    if images:
        media_group = [InputMediaPhoto(file.file_id) for file in images]
        await update.effective_chat.send_media_group(
            media=media_group,
            caption=message_text,
        )
    else:
        await update.effective_chat.send_message(
            text=message_text,
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


async def _get_reported_user_id_and_user_id(
    _context: ContextTypes.DEFAULT_TYPE,
) -> Dict[str, Union[int, str]]:
    reported_user_id: int = _context.user_data["current_profile"].user
    reported_user_name: str = _context.user_data["current_profile"].name
    return {
        "reported_user_id": reported_user_id,
        "reported_user_name": reported_user_name,
    }


async def _clear_complain_info_context(_context):
    _context.user_data.pop("complain_info", None)
