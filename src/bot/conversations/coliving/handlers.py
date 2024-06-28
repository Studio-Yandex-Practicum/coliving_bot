from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import conversations.coliving.buttons as buttons
import conversations.coliving.callback_funcs as callback_funcs
import conversations.common_functions.common_buttons as common_buttons
import conversations.common_functions.common_funcs as common_funcs
from conversations.coliving.coliving_common import coliving_common
from conversations.coliving.coliving_current_user import callback_funcs as current_user
from conversations.coliving.coliving_roommate import callback_funcs as coliving_roommate
from conversations.coliving.coliving_transfer import callback_funcs as coliving_transfer
from conversations.coliving.states import States
from conversations.common_functions.common_buttons import RETURN_TO_MENU_BTN
from conversations.menu.buttons import COLIVING_BUTTON
from conversations.menu.constants import CANCEL_COMMAND, MENU_COMMAND

coliving_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            pattern=rf"^{COLIVING_BUTTON}$",
            callback=callback_funcs.start,
        ),
    ],
    states={
        States.LOCATION: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_location,
                pattern=common_buttons.LOCATION_CALLBACK_PATTERN,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callback_funcs.handle_location_text_input_instead_of_choosing_button,
            ),
        ],
        States.ROOM_TYPE: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_room_type,
                pattern=common_buttons.ROOM_TYPE_CALLBACK_PATTERN,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callback_funcs.handle_room_type_text_input_instead_of_choosing_button,
            ),
        ],
        States.ABOUT_ROOM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callback_funcs.handle_about_coliving,
            ),
        ],
        States.PRICE: [
            MessageHandler(
                filters.Regex(r"^(\d*)$") & ~filters.COMMAND,
                callback_funcs.handle_price,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callback_funcs.handle_price,
            ),
        ],
        States.PHOTO_ROOM: [
            MessageHandler(
                filters.PHOTO,
                callback_funcs.handle_photo_room,
            ),
            MessageHandler(
                filters.Regex(rf"{buttons.SAVE_PHOTO_BUTTON}") & ~filters.COMMAND,
                callback_funcs.send_received_room_photos,
            ),
        ],
        States.CONFIRMATION: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_confirm_or_edit_reply_confirm,
                pattern=rf"^{buttons.BTN_LABEL_CONFIRM}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_profile_confirmation_cancel,
                pattern=rf"^{buttons.BTN_LABEL_CANCEL_CREATE}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callback_funcs.handle_confirm_or_cancel_profile_text_instead_of_button,
            ),
        ],
        States.EDIT: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_delete_profile,
                pattern=rf"^{buttons.BTN_LABEL_DELETE_PROFILE_KEYBOARD}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_what_to_edit_room_type,
                pattern=rf"^{buttons.BTN_LABEL_EDIT_ROOM_TYPE}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_what_to_edit_location,
                pattern=rf"^{buttons.BTN_LABEL_EDIT_LOCATION}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_what_to_edit_about_room,
                pattern=rf"^{buttons.BTN_LABEL_EDIT_ABOUT_ROOM}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_what_to_edit_price,
                pattern=rf"^{buttons.BTN_LABEL_EDIT_PRICE}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_what_to_edit_photo_room,
                pattern=rf"^{buttons.BTN_LABEL_EDIT_PHOTO}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callback_funcs.handle_what_to_edit_text_instead_of_button,
            ),
            CallbackQueryHandler(
                callback=common_funcs.handle_return_to_menu_response,
                pattern=rf"^{RETURN_TO_MENU_BTN}$",
            ),
        ],
        States.IS_VISIBLE: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_is_visible_coliving_profile_yes,
                pattern=(
                    rf"^({common_buttons.SHOW_SEARCH_BUTTON}"
                    rf"|{common_buttons.HIDE_SEARCH_BUTTON})$"
                ),
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callback_funcs.repeat_question_about_coliving_visibility,
            ),
        ],
        States.EDIT_LOCATION: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_edit_location,
                pattern=common_buttons.LOCATION_CALLBACK_PATTERN,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callback_funcs.handle_location_text_input_instead_of_choosing_button,
            ),
        ],
        States.EDIT_ROOM_TYPE: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_edit_select_room_type,
                pattern=common_buttons.ROOM_TYPE_CALLBACK_PATTERN,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callback_funcs.handle_room_type_text_input_instead_of_choosing_button,
            ),
        ],
        States.EDIT_ABOUT_ROOM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callback_funcs.handle_edit_about_coliving,
            ),
        ],
        States.EDIT_PRICE: [
            MessageHandler(
                filters.Regex(r"^(\d*)$") & ~filters.COMMAND,
                callback_funcs.handle_edit_price,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callback_funcs.handle_edit_price,
            ),
        ],
        States.EDIT_PHOTO_ROOM: [
            MessageHandler(
                filters.PHOTO,
                callback_funcs.handle_edit_photo_room,
            ),
            MessageHandler(
                filters.Regex(rf"^{buttons.SAVE_EDITED_PHOTO_BUTTON}")
                & ~filters.COMMAND,
                callback_funcs.send_edited_room_photos,
            ),
        ],
        States.EDIT_CONFIRMATION: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_edit_profile_confirmation_confirm,
                pattern=rf"^{buttons.BTN_LABEL_CONFIRM}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_edit_profile_confirmation_cancel,
                pattern=rf"^{buttons.BTN_LABEL_CANCEL_EDIT}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_edit_profile_confirmation_continue_edit,
                pattern=rf"^{buttons.BTN_LABEL_EDIT_CONTINUE}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callback_funcs.handle_edit_profile_confirmation_text_instead_of_button,
            ),
        ],
        States.DELETE_COLIVING: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_delete_coliving_confirmation_confirm,
                pattern=rf"^{buttons.BTN_LABEL_DELETE_CONFIRM}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_delete_coliving_confirmation_cancel,
                pattern=rf"^{buttons.BTN_LABEL_DELETE_CANCEL}",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callback_funcs.handle_delete_profile,
            ),
        ],
        States.NEXT_ROOMMATE: [
            CallbackQueryHandler(
                callback=callback_funcs.next_roommate,
                pattern=rf"^{buttons.YES_BTN}$",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.end_of_assign_roommate,
                pattern=rf"^{buttons.NO_BTN}$",
            ),
        ],
        States.NO_ROOMMATES: [
            CallbackQueryHandler(
                callback=callback_funcs.end_of_assign_roommate,
                pattern=rf"^{buttons.WAIT_BTN}$",
            ),
        ],
        States.ROOMMATE: [
            CallbackQueryHandler(
                callback=callback_funcs.roommate_like,
                pattern=rf"^{buttons.OK_ROOMMATE_BTN}$",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.next_roommate,
                pattern=rf"^{buttons.NEXT_ROOMMATE_BTN}$",
            ),
        ],
        States.COLIVING: [
            CallbackQueryHandler(
                callback=callback_funcs.handle_coliving_edit,
                pattern=rf"^{buttons.BTN_LABEL_EDIT_PROFILE_KEYBOARD}",
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_is_visible_switching,
                pattern=(
                    rf"^({common_buttons.SHOW_SEARCH_BUTTON}"
                    rf"|{common_buttons.HIDE_SEARCH_BUTTON})$"
                ),
            ),
            CallbackQueryHandler(
                callback=callback_funcs.handle_assign_roommate,
                pattern=rf"^{buttons.BTN_LABEL_ASSIGN_ROOMMATE}$",
            ),
            CallbackQueryHandler(
                callback=coliving_transfer.handle_coliving_transfer_to,
                pattern=r"^transfer_to",
            ),
            CallbackQueryHandler(
                callback=common_funcs.handle_return_to_menu_response,
                pattern=rf"^{RETURN_TO_MENU_BTN}$",
            ),
            CallbackQueryHandler(
                callback=coliving_roommate.handle_coliving_roommates,
                pattern=r"^roommates_profiles",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
                callback_funcs.handle_coliving_text_instead_of_button,
            ),
        ],
        States.COLIVING_ROOMMATE: [
            CallbackQueryHandler(
                callback=coliving_roommate.get_profile_roommate_admin_handler,
                pattern=r"^profile:(?P<telegram_id>\d+)$",
            ),
            CallbackQueryHandler(
                callback=coliving_roommate.unpin_profile,
                pattern=r"^profile_unpin_coliving:(?P<telegram_id>\d+)$",
            ),
            CallbackQueryHandler(
                callback=coliving_common.unpin_profile_no,
                pattern=r"^unpin_profile_no",
            ),
            CallbackQueryHandler(
                callback=coliving_common.unpin_profile_yes,
                pattern=r"^unpin_profile_yes:(?P<telegram_id>\d+)$",
            ),
            CallbackQueryHandler(
                callback=coliving_common.coliving_transfer_page_callback_handler,
                pattern=r"^coliving_page:(?P<page>\d+)",
            ),
            CallbackQueryHandler(
                callback=coliving_roommate.handle_coliving_roommates,
                pattern=r"^roommates_profiles",
            ),
        ],
        States.TRANSFER_COLIVING: [
            CallbackQueryHandler(
                callback=coliving_common.coliving_transfer_page_callback_handler,
                pattern=r"^coliving_page:(?P<page>\d+)",
            ),
            CallbackQueryHandler(
                callback=coliving_transfer.handle_coliving_transfer_to_confirm,
                pattern=r"^profile:(?P<telegram_id>\d+)",
            ),
            CallbackQueryHandler(
                callback=coliving_transfer.handle_coliving_set_new_owner,
                pattern=r"^set_new_owner",
            ),
            CallbackQueryHandler(
                callback=coliving_transfer.handle_cancel_coliving_transfer,
            ),
        ],
        States.COLIVING_CURRENT_USER: [
            # BUG: Использование такой же функции обратного вызова,
            # что и для случая с организатором коливинга приводит к тому,
            # что обычный проживающий получает права открепить любого соседа.
            # А должен иметь право только посмотреть анкету и вернуться.
            #
            CallbackQueryHandler(
                callback=current_user.get_profile_roommate_cur_user_handler,
                pattern=r"^profile:(?P<telegram_id>\d+)$",
            ),
            CallbackQueryHandler(
                callback=current_user.current_user_roommates_handler,
                pattern=r"^roommates_profiles",
            ),
            CallbackQueryHandler(
                callback=coliving_common.unpin_profile_yes,
                pattern=r"^unpin_profile_yes:(?P<telegram_id>\d+)",
            ),
            CallbackQueryHandler(
                callback=coliving_common.unpin_profile_no,
                pattern=r"^unpin_profile_no",
            ),
            CallbackQueryHandler(
                callback=current_user.unpin_me,
                pattern=r"^unpin_me",
            ),
            CallbackQueryHandler(
                callback=common_funcs.handle_return_to_menu_response,
                pattern=rf"^{RETURN_TO_MENU_BTN}$",
            ),
        ],
    },
    fallbacks=[
        CommandHandler(
            command=CANCEL_COMMAND,
            callback=common_funcs.cancel,
        ),
        CommandHandler(
            command=MENU_COMMAND,
            callback=common_funcs.return_to_menu_via_menu_command,
        ),
    ],
)
