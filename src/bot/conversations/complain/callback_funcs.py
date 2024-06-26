from typing import Dict, Union

from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from conversations.common_functions.common_funcs import add_response_prefix
from conversations.complain import states
from conversations.complain.keyboards import (
    CATEGORY_KEYBOARD,
    SCREENSHOT_OR_NOT_KEYBOARD,
    get_report_or_not_keyboard,
)
from conversations.complain.templates import (
    ASK_COMPLAIN_TEXT,
    ASK_SCREENSHOT,
    CATEGORY_CHOOSE_TEXT,
    COMPLAIN_ERROR_TEXT,
    COMPLAIN_TEXT,
    CREATE_REPORT_TEXT,
    REPORT_DATA,
    SCREENSHOT_ATTACH_TEXT,
    USER_ALREADY_REPORTED,
)
from internal_requests import api_service
from internal_requests.entities import Categories, Image, Report


async def complain(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """
    Начало жалобы, проверяет - осуществляется ли просмотр анкеты.
    """
    await update.effective_message.reply_text(
        text=CREATE_REPORT_TEXT,
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
    category = _context.user_data.get("category", Categories.CATEGORY_OTHER)
    _context.user_data["complain_info"] = Report(
        reported_user=reported_user_dict["reported_user_id"],
        reporter=update.effective_chat.id,
        text="",
        category=category,
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
    await update.effective_message.edit_text(
        text=CATEGORY_CHOOSE_TEXT,
        reply_markup=CATEGORY_KEYBOARD,
    )
    return states.CATEGORY


async def handle_category(
    update: Update,
    _context: ContextTypes.DEFAULT_TYPE,
):
    category_name = update.callback_query.data
    category = Categories(category_name)
    _context.user_data["complain_info"].category = category
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
    await update.effective_message.reply_text(
        text=SCREENSHOT_ATTACH_TEXT,
        reply_markup=SCREENSHOT_OR_NOT_KEYBOARD,
    )
    return states.SCREENSHOT


@add_response_prefix()
async def attach_screenshot(
    update: Update,
    _context: ContextTypes.DEFAULT_TYPE,
):
    await update.effective_message.reply_text(
        text=ASK_SCREENSHOT,
    )


async def handle_screenshot(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    new_screenshot = update.effective_message.photo[-1]
    _context.user_data["complain_info"].screenshot = Image(
        file_id=new_screenshot.file_id, photo_size=new_screenshot
    )
    report = _context.user_data["complain_info"]
    response = await api_service.create_report(report=report)
    if response.status_code == 208:
        await update.effective_chat.send_message(
            text=USER_ALREADY_REPORTED,
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await update.effective_chat.send_photo(
            photo=_context.user_data["complain_info"].screenshot.file_id,
            caption=REPORT_DATA.format(
                user_id=_context.user_data["complain_info"].reported_user,
                category=_context.user_data["complain_info"].category.value,
                text=_context.user_data["complain_info"].text,
            ),
        )
    return ConversationHandler.END


@add_response_prefix()
async def final_report(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    message_text = REPORT_DATA.format(
        user_id=_context.user_data["complain_info"].reported_user,
        category=_context.user_data["complain_info"].category.value,
        text=_context.user_data["complain_info"].text,
    )
    report = _context.user_data["complain_info"]
    response = await api_service.create_report(report)
    if response.status_code == 208:
        await update.effective_chat.send_message(
            text=USER_ALREADY_REPORTED,
            reply_markup=ReplyKeyboardRemove(),
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
