from datetime import datetime

from internal_requests.entities import ColivingProfile, UserProfile


async def get_user_coliving_info_by_tg_id(telegram_id: int) -> ColivingProfile:
    """Получает данные о telegram-пользователе."""

    return ColivingProfile(
        roommates="Сосед Иван",
        location="Санкт-Петербург",
        price=2500,
        room_type="Спальное место в комнате",
        about="Очень уютная раскривушка)",
        is_visible="Да",
        viewers=None,
        created_date=datetime.now(),
    )


async def get_user_coliving_status(telegram_id: int) -> UserProfile:
    """Получает данные о telegram-пользователе."""

    ####################################################################
    # Поменять для.
    # is_сoliving=False для создания профиля
    # is_сoliving=True для просмотра профиля
    ####################################################################

    return UserProfile(
        is_сoliving=False
        # is_сoliving=True
    )
