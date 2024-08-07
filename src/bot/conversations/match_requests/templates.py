from internal_requests.entities import ProfileSearchSettings

ASK_RESPOND_TO_LIKE = "Что ты хочешь сделать?"
END_OF_SEARCH = (
    "Надеюсь, ты смог найти себе соседа.\n"
    "А если нет, помни, что ты всегда можешь начать поиск заново."
)
LIKE_NOTIFICATION = "Кто-то хочет стать твоим соседом, посмотрим?"

BUTTON_ERROR_MSG = "Выбери соответствующий вариант."

NEW_MATCH_NOTIFICATION = (
    "У вас взаимный лайк с {username} и он/она"
    " твой потенциальный сосед, напишите ему/ей 🤝"
)

REJECTION_NOTIFICATION = (
    "<b>Вы отклонили анкету пользователя {sender_profile.name}.</b>"
)

NEIGHBOR_WANTS_TO_BE = "Твоим соседом хочет стать:"

SMTH_WRONG_WITH_USER_LIKE = (
    "Похоже, этим пользователем что-то случилось. Возможно, он был заблокирован."
)


def format_search_settings_message(filters: ProfileSearchSettings) -> str:
    """Формирует сообщение с настройками поиска."""
    result = f"""
    <b>Текущие настройки поиска соседа:</b>

    <b>Город:</b> {filters.location}
    <b>Пол соседа:</b> {filters.sex}
    """
    if filters.age_max is None:
        result += f"<b>Возраст:</b> >{filters.age_min}"
    else:
        result += f"<b>Возраст:</b> {filters.age_min}-{filters.age_max}"
    return result
