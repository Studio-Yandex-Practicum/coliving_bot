from internal_requests.entities import UserProfile


async def get_user_profile_by_telegram_id(telegram_id: int) -> UserProfile:
    return UserProfile(
        name="Володя",
        sex="Я парень",
        age=25,
        location="Москва",
        about="Немного о себе",
        is_visible=False,
    )
