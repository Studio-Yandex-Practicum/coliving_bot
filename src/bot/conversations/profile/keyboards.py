from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from conversations.common_functions.common_buttons import (
    HIDE_SEARCH_BUTTON,
    RETURN_BTN_LABEL,
    RETURN_TO_MENU_BTN,
    SHOW_SEARCH_BUTTON,
)
from conversations.common_functions.common_keyboards import HIDE_BUTTON, SEARCH_BUTTON
from conversations.profile.buttons import (
    CANCEL_PROFILE_CREATION,
    DELETE_CANCEL_BUTTON,
    DELETE_CONFIRM_BUTTON,
    DELETE_PROFILE_BUTTON,
    EDIT_ABOUT_BUTTON,
    EDIT_AGE_BUTTON,
    EDIT_CANCEL_BUTTON,
    EDIT_FORM_BUTTON,
    EDIT_LOCATION_BUTTON,
    EDIT_NAME_BUTTON,
    EDIT_RESUME_BUTTON,
    EDIT_SEX_BUTTON,
    FEMALE_BUTTON,
    MALE_BUTTON,
    NEW_PHOTO_BUTTON,
    SAVE_EDITED_PHOTO_BUTTON,
    SAVE_PHOTO_BUTTON,
    YES_BUTTON,
)

PROFILE_DUPLICATE_BUTTONS = [
    InlineKeyboardButton(text=EDIT_FORM_BUTTON, callback_data=EDIT_FORM_BUTTON),
    InlineKeyboardButton(text=RETURN_TO_MENU_BTN, callback_data=RETURN_TO_MENU_BTN),
]

VISIBLE_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(HIDE_BUTTON, *PROFILE_DUPLICATE_BUTTONS)
)

HIDDEN_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(SEARCH_BUTTON, *PROFILE_DUPLICATE_BUTTONS)
)

SEX_KEYBOARD = InlineKeyboardMarkup.from_row(
    button_row=(
        InlineKeyboardButton(text=MALE_BUTTON, callback_data=MALE_BUTTON),
        InlineKeyboardButton(text=FEMALE_BUTTON, callback_data=FEMALE_BUTTON),
    )
)

PHOTO_KEYBOARD = ReplyKeyboardMarkup.from_button(
    KeyboardButton(text=SAVE_PHOTO_BUTTON), resize_keyboard=True
)

FORM_SAVED_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=YES_BUTTON, callback_data=YES_BUTTON),
        InlineKeyboardButton(
            text=CANCEL_PROFILE_CREATION, callback_data=CANCEL_PROFILE_CREATION
        ),
    )
)

FORM_VISIBLE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=SHOW_SEARCH_BUTTON, callback_data=SHOW_SEARCH_BUTTON),
        InlineKeyboardButton(text=HIDE_SEARCH_BUTTON, callback_data=HIDE_SEARCH_BUTTON),
    )
)

PHOTO_EDIT_KEYBOARD = ReplyKeyboardMarkup.from_button(
    KeyboardButton(text=SAVE_EDITED_PHOTO_BUTTON), resize_keyboard=True
)

FORM_EDIT_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=EDIT_ABOUT_BUTTON, callback_data=EDIT_ABOUT_BUTTON),
        InlineKeyboardButton(text=EDIT_NAME_BUTTON, callback_data=EDIT_NAME_BUTTON),
        InlineKeyboardButton(text=EDIT_SEX_BUTTON, callback_data=EDIT_SEX_BUTTON),
        InlineKeyboardButton(text=EDIT_AGE_BUTTON, callback_data=EDIT_AGE_BUTTON),
        InlineKeyboardButton(
            text=EDIT_LOCATION_BUTTON, callback_data=EDIT_LOCATION_BUTTON
        ),
        InlineKeyboardButton(text=NEW_PHOTO_BUTTON, callback_data=NEW_PHOTO_BUTTON),
        InlineKeyboardButton(
            text=DELETE_PROFILE_BUTTON, callback_data=DELETE_PROFILE_BUTTON
        ),
        InlineKeyboardButton(text=RETURN_BTN_LABEL, callback_data=RETURN_BTN_LABEL),
    )
)

FORM_SAVE_OR_EDIT_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=YES_BUTTON, callback_data=YES_BUTTON),
        InlineKeyboardButton(text=EDIT_CANCEL_BUTTON, callback_data=EDIT_CANCEL_BUTTON),
        InlineKeyboardButton(text=EDIT_RESUME_BUTTON, callback_data=EDIT_RESUME_BUTTON),
    )
)

DELETE_OR_CANCEL_PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(
            text=DELETE_CONFIRM_BUTTON,
            callback_data=DELETE_CONFIRM_BUTTON,
        ),
        InlineKeyboardButton(
            text=DELETE_CANCEL_BUTTON,
            callback_data=DELETE_CANCEL_BUTTON,
        ),
    )
)
