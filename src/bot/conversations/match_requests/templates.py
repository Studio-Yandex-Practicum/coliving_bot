from internal_requests.entities import SearchSettings

END_OF_SEARCH = (
    "Надеюсь, ты смог найти себе соседа.\n"
    "А если нет, помни, что ты всегда можешь начать поиск заново."
)
LIKE_NOTIFICATION = "Кто-то хочет стать твоим соседом, посмотрим?"
SENDER_PROFILE = "Смотрим анкету {sender_profile.name}"
BUTTON_ERROR_MSG = "Выбери соответствующий вариант."
SEND_SENDER = "Приветствуем будущего соседа {sender_id}"
SEND_RECIVER = (
    "Приветствуем будущего соседа {reciver_id},\n" "Ему тоже понравилась твоя анкета!"
)


def format_search_settings_message(filters: SearchSettings) -> str:
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
