from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import conversations.coliving.templates as templates
from conversations.coliving.templates import ROOM_TYPE_CALLBACK_DATA
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
            callback_data=(
                f"{ROOM_TYPE_CALLBACK_DATA}:{templates.BTN_LABEL_BED_IN_ROOM}"
            ),
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_ROOM_IN_APPARTMENT,
            callback_data=(
                f"{ROOM_TYPE_CALLBACK_DATA}:{templates.BTN_LABEL_ROOM_IN_APPARTMENT}"
            ),
        ),
    )
)

EDIT_PROFILE_KEYBOARD = InlineKeyboardButton(
    text=templates.BTN_LABEL_EDIT_PROFILE_KEYBOARD,
    callback_data=templates.BTN_LABEL_EDIT_PROFILE_KEYBOARD,
)

CONFIRM_OR_EDIT_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        CONFIRMATION_KEYBOARD,
        EDIT_PROFILE_KEYBOARD,
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

SHOW_SEARCH_KEYBOARD = InlineKeyboardButton(
    text=templates.BTN_LABEL_SHOW,
    callback_data="True",
)

HIDE_SEARCH_KEYBOARD = InlineKeyboardButton(
    text=templates.BTN_LABEL_HIDE_SEARCH_KEYBOARD,
    callback_data="False",
)

IS_VISIBLE_OR_NOT_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        SHOW_SEARCH_KEYBOARD,
        HIDE_SEARCH_KEYBOARD,
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

COLIVING_PROFILE_KEYBOARD_VISIBLE = InlineKeyboardMarkup.from_column(
    button_column=(
        EDIT_PROFILE_KEYBOARD,
        HIDE_SEARCH_KEYBOARD,
        InlineKeyboardButton(
            text=templates.BTN_LABEL_ROOMMATES, callback_data=templates.BTN_ROOMMATES
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_VIEWS, callback_data=templates.BTN_VIEWS
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_TRANSFER_TO,
            callback_data=templates.BTN_TRANSFER_TO,
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_GO_TO_MENU, callback_data=templates.BTN_GO_TO_MENU
        ),
    )
)

COLIVING_PROFILE_KEYBOARD_NOT_VISIBLE = InlineKeyboardMarkup.from_column(
    button_column=(
        EDIT_PROFILE_KEYBOARD,
        SHOW_SEARCH_KEYBOARD,
        InlineKeyboardButton(
            text=templates.BTN_LABEL_ROOMMATES, callback_data=templates.BTN_ROOMMATES
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_VIEWS, callback_data=templates.BTN_VIEWS
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_TRANSFER_TO,
            callback_data=templates.BTN_TRANSFER_TO,
        ),
        InlineKeyboardButton(
            text=templates.BTN_LABEL_GO_TO_MENU, callback_data=templates.BTN_GO_TO_MENU
        ),
    )
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
    text=templates.BTN_LABEL_DELETE_CONFIRM, callback_data=templates.BTN_DELETE_CONFIRM
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


async def create_keyboard_of_locations():
    locations = await api_service.get_locations()
    button_column = []
    for location in locations:
        button_column.append(
            InlineKeyboardButton(
                text=location.name,
                callback_data=f"{templates.LOCATION_CALLBACK_DATA}:{location.name}",
            )
        )
    return InlineKeyboardMarkup.from_column(button_column=button_column)
