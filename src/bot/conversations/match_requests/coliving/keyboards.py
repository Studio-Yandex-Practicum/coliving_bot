from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from conversations.match_requests.buttons import SEE_PROFILE_BNT

HOST_LIKE_NOTIFY = "host_like_notify"


async def get_view_coliving_keyboard(like, sender_id) -> InlineKeyboardMarkup:
    view_coliving_keyboard = InlineKeyboardMarkup.from_column(
        button_column=(
            InlineKeyboardButton(
                text=SEE_PROFILE_BNT,
                callback_data=f"{like.id}:{sender_id}:{HOST_LIKE_NOTIFY}",
            ),
        )
    )
    return view_coliving_keyboard
