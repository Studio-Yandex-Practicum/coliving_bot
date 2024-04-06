from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import conversations.coliving.templates as templates
from conversations.common_functions.common_buttons import (
    LOCATION_PREFIX,
    ROOM_TYPE_PREFIX,
)
from conversations.common_functions.common_keyboards import HIDE_BUTTON, SEARCH_BUTTON
from conversations.common_functions.common_templates import RETURN_TO_MENU_BTN_LABEL
from internal_requests import api_service

CONFIRMATION_KEYBOARD = InlineKeyboardButton(
    text=templates.BTN_LABEL_CONFIRM, callback_data=templates.BTN_LABEL_CONFIRM
)

CANCEL_KEYBOARD = InlineKeyboardButton(
    text=templates.BTN_LABEL_CANCEL, callback_data=templates.BTN_CANCEL
)

ROOM_TYPE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=templates.BTN_LABEL_BED_IN_ROOM,
            callback_data=f"{ROOM_TYPE_PREFIX}:{templates.BTN_LABEL_BED_IN_ROOM}",
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_ROOM_IN_APARTMENT,
            callback_data=(
                f"{ROOM_TYPE_PREFIX}:{templates.BTN_LABEL_ROOM_IN_APARTMENT}"
            ),
        ),
    )
)

EDIT_PROFILE_KEYBOARD = InlineKeyboardButton(
    text=templates.BTN_LABEL_EDIT_PROFILE_KEYBOARD,
    callback_data=templates.BTN_LABEL_EDIT_PROFILE_KEYBOARD,
)

CONFIRM_OR_CANCEL_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        CONFIRMATION_KEYBOARD,
        InlineKeyboardButton(
            text=templates.BTN_LABEL_CANCEL_CREATE,
            callback_data=templates.BTN_LABEL_CANCEL_CREATE,
        ),
    )
)

WHAT_EDIT_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=templates.BTN_LABEL_FILL_AGAIN,
            callback_data=templates.BTN_LABEL_FILL_AGAIN,
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_EDIT_LOCATION,
            callback_data=templates.BTN_LABEL_EDIT_LOCATION,
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_EDIT_ROOM_TYPE,
            callback_data=templates.BTN_LABEL_EDIT_ROOM_TYPE,
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_EDIT_ABOUT_ROOM,
            callback_data=templates.BTN_LABEL_EDIT_ABOUT_ROOM,
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_EDIT_PRICE,
            callback_data=templates.BTN_LABEL_EDIT_PRICE,
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_EDIT_PHOTO,
            callback_data=templates.BTN_LABEL_EDIT_PHOTO,
        ),
    )
)

IS_VISIBLE_OR_NOT_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        HIDE_BUTTON,
        SEARCH_BUTTON,
    )
)

EDIT_CONFIRMATION_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        CONFIRMATION_KEYBOARD,
        InlineKeyboardButton(
            text=templates.BTN_LABEL_CANCEL_EDIT,
            callback_data=templates.BTN_LABEL_CANCEL_EDIT,
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_EDIT_CONTINUE,
            callback_data=templates.BTN_LABEL_EDIT_CONTINUE,
        ),
    )
)

COLIVING_PROFILE_DUPLICATE_BUTTONS = [
    InlineKeyboardButton(
        text=templates.BTN_LABEL_ROOMMATES, callback_data=templates.BTN_ROOMMATES
    ),
    InlineKeyboardButton(
        text=templates.BTN_LABEL_ASSIGN_ROOMMATE,
        callback_data=templates.BTN_ASSIGN_ROOMMATE
    ),
    InlineKeyboardButton(
        text=templates.BTN_LABEL_TRANSFER_TO,
        callback_data=templates.BTN_TRANSFER_TO,
    ),
    EDIT_PROFILE_KEYBOARD,
    InlineKeyboardButton(
        text=templates.BTN_LABEL_DELETE_PROFILE_KEYBOARD,
        callback_data=templates.BTN_LABEL_DELETE_PROFILE_KEYBOARD,
    ),
    InlineKeyboardButton(
        text=RETURN_TO_MENU_BTN_LABEL, callback_data=templates.BTN_GO_TO_MENU
    ),
]

COLIVING_PROFILE_KEYBOARD_VISIBLE = InlineKeyboardMarkup.from_column(
    button_column=(SEARCH_BUTTON, *COLIVING_PROFILE_DUPLICATE_BUTTONS)
)

COLIVING_PROFILE_KEYBOARD_NOT_VISIBLE = InlineKeyboardMarkup.from_column(
    button_column=(HIDE_BUTTON, *COLIVING_PROFILE_DUPLICATE_BUTTONS)
)

INVITE_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardButton(
    text=templates.BTN_LABEL_INVITE_ROOMMATES,
    callback_data=templates.BTN_INVITE_ROOMMATES,
)

# Выбор

# CHOOSE_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [

#             InlineKeyboardButton(
#                 text='Выбран',
#                 callback_data=BTN_CONFIRM
#             ),
#         ]
#     ]
# )

DELETE_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardButton(
    text=templates.BTN_LABEL_DELETE_ROOMMATES,
    callback_data=templates.BTN_DELETE_ROOMMATES,
)

REPORT_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardButton(
    text=templates.BTN_LABEL_REPORT_ROOMMATES,
    callback_data=templates.BTN_REPORT_ROOMMATES,
)

CONFIRMATION_DELETE_KEYBOARD = InlineKeyboardButton(
    text=templates.BTN_LABEL_DELETE_CONFIRM,
    callback_data=templates.BTN_LABEL_DELETE_CONFIRM,
)

ROOMMATES_INVITE_REPORT_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        INVITE_ROOMMATES_PROFILE_KEYBOARD,
        REPORT_ROOMMATES_PROFILE_KEYBOARD,
    )
)

ROOMMATES_INVITE_REPORT_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        DELETE_ROOMMATES_PROFILE_KEYBOARD,
        REPORT_ROOMMATES_PROFILE_KEYBOARD,
    )
)

CONFIRM_ROOMMATES_INVITE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        CONFIRMATION_KEYBOARD,
        CANCEL_KEYBOARD,
    )
)

REPORT_OR_CANCEL_ROOMMATES_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        REPORT_ROOMMATES_PROFILE_KEYBOARD,
        CANCEL_KEYBOARD,
    )
)

SAVE_OR_CANCEL_PHOTO_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=templates.SAVE_PHOTO_BUTTON, callback_data=templates.SAVE_PHOTO_BUTTON
        ),
        CANCEL_KEYBOARD,
    )
)

SAVE_OR_CANCEL_NEW_PHOTO_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=templates.SAVE_EDITED_PHOTO_BUTTON,
            callback_data=templates.SAVE_EDITED_PHOTO_BUTTON,
        ),
        CANCEL_KEYBOARD,
    )
)

DELETE_OR_CANCEL_COLIVING_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=templates.BTN_LABEL_DELETE_CONFIRM,
            callback_data=templates.BTN_LABEL_DELETE_CONFIRM,
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_DELETE_CANCEL,
            callback_data=templates.BTN_LABEL_DELETE_CANCEL,
        ),
    )
)


async def create_keyboard_of_locations():
    locations = await api_service.get_locations()
    button_column = []
    for location in locations:
        button_column.append(
            InlineKeyboardButton(
                text=location.name,
                callback_data=f"{LOCATION_PREFIX}:{location.name}",
            )
        )
    return InlineKeyboardMarkup.from_column(button_column=button_column)
