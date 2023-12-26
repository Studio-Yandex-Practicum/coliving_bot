from datetime import datetime

from .entities import UserProfile


async def get_filtered_users(
    searcher_id: int,
    location: str,
    sex: str,
    age_min: int,
    age_max: int,
) -> list[UserProfile]:
    return [
        UserProfile(
            name="Иван",
            age=25,
            sex="Парень",
            location="Москва",
            about="Я Ваня!",
            images="D:/Dev/PraktikumPlus/coliving_bot/src/.data/imgs/cat.jpg",
            telegram_id=111,
        ),
        UserProfile(
            name="Владимир",
            age=24,
            sex="Парень",
            location="Москва",
            about="А я Вова!",
            images="D:/Dev/PraktikumPlus/coliving_bot/src/.data/imgs/pepe.jpg",
            telegram_id=222,
        ),
    ]


async def post_match_request(
    sender_id: int,
    reciever_id: int,
    status: int = 0,
    created_date: datetime = datetime.now(),
    match_date: datetime | None = None,
) -> int:
    return 1
