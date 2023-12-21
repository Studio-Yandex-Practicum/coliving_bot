from datetime import datetime

from internal_requests.entities import ColivingProfile, UserProfile


async def get_user_coliving_info_by_tg_id(telegram_id: int) -> ColivingProfile:
    """Получает данные о telegram-пользователе."""

    return ColivingProfile(
        roommates="Сосед Иван",
        location="Санкт-Петербург",
        price=5500,
        room_type="Комната в квартире",
        about="Ну очень уютно",
        is_visible=True,
        viewers=None,
        created_date=datetime.now(),
    )

    # return ColivingProfile(
    #         roommates=None,
    #         location=None,
    #         price=None,
    #         room_type=None,
    #         about=None,
    #         is_visible=None,
    #         viewers=None,
    #         created_date=None,
    #     )


# async def get_user_coliving_info_by_tg_id(telegram_id: int) -> TestColivingProfile:
#     """Получает данные о telegram-пользователе."""

#     return TestColivingProfile(
#             roommates='Сосед Иван',
#             location='Москва',
#             price=5500,
#             room_type='Комната в квартире',
#             about='Ну очень уютно',
#             is_visible=True,
#             viewers=True,
#             created_date=datetime.now()
#         )


async def get_user_coliving_status(telegram_id: int) -> UserProfile:
    """Получает данные о telegram-пользователе."""

    return UserProfile(
        # is_сoliving=False
        is_сoliving=True
    )
