from telegram import Update
from telegram.ext import CallbackContext, ContextTypes, ConversationHandler

import conversations.coliving.coliving_transfer.templates as templates
from conversations.coliving import keyboards as keyboards
from conversations.coliving.buttons import BTN_LABEL_CANCEL, BTN_LABEL_CONFIRM
from conversations.coliving.coliving_common.coliving_common import handle_coliving
from conversations.coliving.states import States
from conversations.common_functions.common_funcs import add_response_prefix
from internal_requests import api_service


async def handle_coliving_transfer_to(update, context):
    """Обработка ответа: Передача коливинга."""
    return await handle_coliving(
        update=update,
        context=context,
        text=templates.SELECT_USER_MESSAGE,
        state=States.TRANSFER_COLIVING,
    )


async def handle_coliving_transfer_to_confirm(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Обработка выбора нового владельца коливинга."""
    telegram_id = int(context.matches[0].group("telegram_id"))
    user_info = await api_service.get_user_profile_by_telegram_id(telegram_id)
    context.user_data["coliving_info"].host = telegram_id
    await update.effective_message.edit_text(
        text=templates.USER_INFO_MESSAGE_TEMPLATE.format(
            name=user_info.name, age=user_info.age
        ),
        reply_markup=keyboards.COLIVING_TRANSFER_TO_CONFIRM_KEYBOARD,
    )
    return None


@add_response_prefix(custom_answer=BTN_LABEL_CONFIRM)
async def handle_coliving_set_new_owner(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Обработка выбора нового владельца коливинга."""
    coliving_info = context.user_data["coliving_info"]
    await api_service.update_coliving_info(coliving_info)
    await api_service.update_user_residence(
        telegram_id=coliving_info.host, residence_id=None
    )
    await context.bot.send_message(
        chat_id=coliving_info.host,
        text=templates.NEW_COLIVING_OWNER_MESSAGE,
    )
    await update.effective_message.reply_text(text=templates.OWNER_CHANGED_MESSAGE)
    return ConversationHandler.END


@add_response_prefix(custom_answer=BTN_LABEL_CANCEL)
async def handle_cancel_coliving_transfer(update: Update, _context: CallbackContext):
    """Обработка отмены передачи коливинга."""
    await update.effective_message.reply_text(templates.CANCELLATION_MESSAGE)
    return ConversationHandler.END
