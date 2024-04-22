from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import conversations.match_requests.buttons as buttons
from internal_requests.entities import ProfileLike


async def get_view_profile_keyboard(
    like: ProfileLike, telegram_id: int
) -> InlineKeyboardMarkup:
    view_profile_keyboard = InlineKeyboardMarkup.from_column(
        button_column=(
            InlineKeyboardButton(
                text=buttons.SEE_PROFILE_BNT,
                callback_data=f"{like.id}:{telegram_id}:{buttons.SEE_PROFILE_BNT}",
            ),
        )
    )
    return view_profile_keyboard
