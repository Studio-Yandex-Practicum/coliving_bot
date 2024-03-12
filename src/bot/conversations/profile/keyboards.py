from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from conversations.common_functions.common_templates import (
    RETURN_BTN_LABEL,
    RETURN_TO_MENU_BTN_LABEL,
)
from conversations.profile.buttons import (
    EDIT_ABOUT_BUTTON,
    EDIT_AGE_BUTTON,
    EDIT_CANCEL_BUTTON,
    EDIT_FORM_BUTTON,
    EDIT_LOCATION_BUTTON,
    EDIT_NAME_BUTTON,
    EDIT_RESUME_BUTTON,
    EDIT_SEX_BUTTON,
    FEMALE_BUTTON,
    FILL_AGAIN_BUTTON,
    HIDE_SEARCH_BUTTON,
    MALE_BUTTON,
    MSK_BUTTON,
    NEW_PHOTO_BUTTON,
    SAVE_EDITED_PHOTO_BUTTON,
    SAVE_PHOTO_BUTTON,
    SHOW_SEARCH_BUTTON,
    SPB_BUTTON,
    YES_BUTTON,
    YES_TO_DO_BUTTON,
)

PROFILE_KEYBOARD_OPEN_SEARCH = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=HIDE_SEARCH_BUTTON, callback_data="is_visible:False"),
        InlineKeyboardButton(text=EDIT_FORM_BUTTON, callback_data=EDIT_FORM_BUTTON),
        InlineKeyboardButton(
            text=RETURN_TO_MENU_BTN_LABEL, callback_data=RETURN_TO_MENU_BTN_LABEL
        ),
    )
)

PROFILE_KEYBOARD_HIDE_SEARCH = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=SHOW_SEARCH_BUTTON, callback_data="is_visible:True"),
        InlineKeyboardButton(text=EDIT_FORM_BUTTON, callback_data=EDIT_FORM_BUTTON),
        InlineKeyboardButton(
            text=RETURN_TO_MENU_BTN_LABEL, callback_data=RETURN_TO_MENU_BTN_LABEL
        ),
    )
)

SEX_KEYBOARD = InlineKeyboardMarkup.from_row(
    button_row=(
        InlineKeyboardButton(text=MALE_BUTTON, callback_data=MALE_BUTTON),
        InlineKeyboardButton(text=FEMALE_BUTTON, callback_data=FEMALE_BUTTON),
    )
)

LOCATION_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=MSK_BUTTON, callback_data=MSK_BUTTON),
        InlineKeyboardButton(text=SPB_BUTTON, callback_data=SPB_BUTTON),
    )
)

PHOTO_KEYBOARD = (
    InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text=SAVE_PHOTO_BUTTON, callback_data=SAVE_PHOTO_BUTTON)
    ),
)

FORM_SAVED_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=YES_BUTTON, callback_data=YES_BUTTON),
        InlineKeyboardButton(text=EDIT_FORM_BUTTON, callback_data=EDIT_FORM_BUTTON),
    )
)

FORM_VISIBLE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=YES_TO_DO_BUTTON, callback_data=YES_TO_DO_BUTTON),
        InlineKeyboardButton(text=HIDE_SEARCH_BUTTON, callback_data=HIDE_SEARCH_BUTTON),
    )
)

PHOTO_EDIT_KEYBOARD = (
    InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(
            text=SAVE_EDITED_PHOTO_BUTTON, callback_data=SAVE_EDITED_PHOTO_BUTTON
        )
    ),
)

FORM_EDIT_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=FILL_AGAIN_BUTTON, callback_data=FILL_AGAIN_BUTTON),
        InlineKeyboardButton(text=EDIT_ABOUT_BUTTON, callback_data=EDIT_ABOUT_BUTTON),
        InlineKeyboardButton(text=EDIT_NAME_BUTTON, callback_data=EDIT_NAME_BUTTON),
        InlineKeyboardButton(text=EDIT_SEX_BUTTON, callback_data=EDIT_SEX_BUTTON),
        InlineKeyboardButton(text=EDIT_AGE_BUTTON, callback_data=EDIT_AGE_BUTTON),
        InlineKeyboardButton(
            text=EDIT_LOCATION_BUTTON, callback_data=EDIT_LOCATION_BUTTON
        ),
        InlineKeyboardButton(text=NEW_PHOTO_BUTTON, callback_data=NEW_PHOTO_BUTTON),
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
