from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import conversations.roommate_search.templates as buttons

SEARCH_SETTINGS_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=buttons.OK_SETTINGS_BTN,
                             callback_data=buttons.OK_SETTINGS_BTN),
        InlineKeyboardButton(text=buttons.EDIT_SETTINGS_BTN,
                             callback_data=buttons.EDIT_SETTINGS_BTN),
    )
)

LOCATION_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=buttons.MSK_BTN, callback_data=buttons.MSK_BTN),
        InlineKeyboardButton(text=buttons.SPB_BTN, callback_data=buttons.SPB_BTN),
    )
)

SEX_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=buttons.MALE_BTN, callback_data=buttons.MALE_BTN),
        InlineKeyboardButton(text=buttons.FEMALE_BTN, callback_data=buttons.FEMALE_BTN),
    )
)

PROFILE_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=buttons.LIKE_BTN, callback_data=buttons.LIKE_BTN),
        InlineKeyboardButton(text=buttons.DISLIKE_BTN,
                             callback_data=buttons.DISLIKE_BTN),
    )
)

NO_MATCHES_KEYBOARD = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=buttons.WAIT_BTN, callback_data=buttons.WAIT_BTN),
        InlineKeyboardButton(text=buttons.EDIT_SETTINGS_BTN,
                             callback_data=buttons.EDIT_SETTINGS_BTN),
    )
)

NEXT_PROFILE = InlineKeyboardMarkup.from_column(
    button_column=(
        InlineKeyboardButton(text=buttons.YES_BTN, callback_data=buttons.YES_BTN),
        InlineKeyboardButton(text=buttons.NO_BTN,
                             callback_data=buttons.NO_BTN),
    )
)

AGE_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text=buttons.AGE_18_23_BTN,
                             callback_data=buttons.AGE_18_23_BTN),
        InlineKeyboardButton(text=buttons.AGE_24_29_BTN,
                             callback_data=buttons.AGE_24_29_BTN),
    ],
    [
        InlineKeyboardButton(text=buttons.AGE_30_35_BTN,
                             callback_data=buttons.AGE_30_35_BTN),
        InlineKeyboardButton(text=buttons.AGE_36_40_BTN,
                             callback_data=buttons.AGE_36_40_BTN),
    ],
    [
        InlineKeyboardButton(text=buttons.AGE_41_45_BTN,
                             callback_data=buttons.AGE_41_45_BTN),
        InlineKeyboardButton(text=buttons.AGE_46_50_BTN,
                             callback_data=buttons.AGE_46_50_BTN),
    ],
    [
        InlineKeyboardButton(text=buttons.AGE_51_55_BTN,
                             callback_data=buttons.AGE_51_55_BTN),
        InlineKeyboardButton(text=buttons.AGE_55UP_BTN,
                             callback_data=buttons.AGE_55UP_BTN),
    ],
])
