from internal_requests.entities import ProfileSearchSettings

END_OF_SEARCH = (
    "Надеюсь, ты смог найти себе соседа.\n"
    "А если нет, помни, что ты всегда можешь начать поиск заново."
)
LIKE_NOTIFICATION = "Кто-то хочет стать твоим соседом, посмотрим?"
LIKE_SENDER_PROFILE = "Смотрим анкету <b>{sender_profile.name}</b>"
BUTTON_ERROR_MSG = "Выбери соответствующий вариант."

NEW_MATCH_NOTIFICATION = (
    "<b>Приветствуем твоего будущего соседа @{username},\n"
    "Вы лайкнули анкеты друг друга.</b>"
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
