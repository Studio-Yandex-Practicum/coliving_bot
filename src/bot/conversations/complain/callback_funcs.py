from typing import Dict, Optional, Union

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from conversations.common_functions.common_funcs import add_response_prefix
from conversations.common_functions.common_templates import CANCEL_TEXT
from conversations.complain import states
from conversations.complain.keyboards import (
    CATEGORY_KEYBOARD,
    NO_COMMENT_REPORT,
    SCREENSHOT_OR_NOT_KEYBOARD,
    get_report_or_not_keyboard,
)
from conversations.complain.templates import (
    ASK_COMPLAIN_TEXT,
    ASK_SCREENSHOT,
    CATEGORY_CHOOSE_TEXT,
    COMPLAIN_ERROR_TEXT,
    COMPLAIN_TEXT,
    REPORT_DATA,
    SCREENSHOT_ATTACH_TEXT,
    USER_ALREADY_REPORTED,
)
from internal_requests import api_service
from internal_requests.entities import Categories, Coliving, Image, Report, UserProfile


async def complain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Начало жалобы, проверяет - осуществляется ли просмотр анкеты.
    """
    reported_user = await _get_info_about_reported_user(update, context)
    if reported_user is None:
        await update.effective_chat.send_message(
            text=COMPLAIN_ERROR_TEXT,
        )
        return ConversationHandler.END
    await _clear_complain_info_context(context)
    reported_user_dict = await _get_reported_user_id_and_user_id(reported_user)
    await agree_or_not(update=update, reported_user_dict=reported_user_dict)
    category = context.user_data.get("category", Categories.CATEGORY_OTHER)
    context.user_data["complain_info"] = Report(
        reported_user=reported_user_dict["reported_user_id"],
        reporter=update.effective_chat.id,
        text="",
        category=category,
    )
    return states.START


async def agree_or_not(update: Update, reported_user_dict: Dict[str, Union[int, str]]):
    report_or_not_keyboard = await get_report_or_not_keyboard(
        reported_user_dict["reported_user_id"]
    )
    await update.effective_chat.send_message(
        text=COMPLAIN_TEXT.format(name=reported_user_dict["reported_user_name"]),
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
    if category == Categories.CATEGORY_OTHER:
        await update.effective_message.edit_text(
            text=ASK_COMPLAIN_TEXT,
        )
        return states.COMPLAIN_TEXT
    await update.effective_message.edit_text(
        text=ASK_COMPLAIN_TEXT,
        reply_markup=NO_COMMENT_REPORT,
    )
    return states.NO_COMMENT_REPORT


async def handle_complain_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    text = update.message.text
    context.user_data["complain_info"].text = text
    await update.effective_message.reply_text(
        text=SCREENSHOT_ATTACH_TEXT,
        reply_markup=SCREENSHOT_OR_NOT_KEYBOARD,
    )
    return states.SCREENSHOT


async def skip_report_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["complain_info"].text = ""
    await update.effective_message.edit_text(
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


async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    complain_info = context.user_data.pop("complain_info")
    new_screenshot = update.effective_message.photo[-1]
    complain_info.screenshot = Image(
        file_id=new_screenshot.file_id, photo_size=new_screenshot
    )
    response = await api_service.create_report(report=complain_info)
    if response.status_code == 208:
        await update.effective_chat.send_message(
            text=USER_ALREADY_REPORTED,
        )
    else:
        await update.effective_chat.send_photo(
            photo=complain_info.screenshot.file_id,
            caption=REPORT_DATA.format(
                user_id=complain_info.reported_user,
                category=complain_info.category.value,
                text=complain_info.text,
            ),
        )
    return ConversationHandler.END


async def final_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    complain_info = context.user_data.pop("complain_info")
    message_text = REPORT_DATA.format(
        user_id=complain_info.reported_user,
        category=complain_info.category.value,
        text=complain_info.text,
    )
    response = await api_service.create_report(complain_info)
    if response.status_code == 208:
        await update.effective_message.edit_text(
            text=USER_ALREADY_REPORTED,
        )
    else:
        await update.effective_message.edit_text(
            text=message_text,
        )
    return ConversationHandler.END


async def cancel_complain_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отменяет диалог без удаления Reply-клавиатуры, без чистки всего контекста."""
    await update.effective_message.reply_text(
        text=CANCEL_TEXT,
    )
    await _clear_complain_info_context(context)
    return ConversationHandler.END


async def _get_info_about_reported_user(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> Optional[UserProfile]:
    profile: UserProfile = context.user_data.get(
        "current_profile"
    ) or context.user_data.get("current_roommate")
    if profile:
        if profile.user == update.effective_chat.id:
            return None
        return profile
    coliving: Coliving = context.user_data.get("current_coliving")
    if coliving:
        return await api_service.get_user_profile_by_telegram_id(
            telegram_id=coliving.host
        )
    return None


async def _get_reported_user_id_and_user_id(
    profile: UserProfile,
) -> Dict[str, Union[int, str]]:
    return {
        "reported_user_id": profile.user,
        "reported_user_name": profile.name,
    }


async def _clear_complain_info_context(context):
    context.user_data.pop("complain_info", None)
