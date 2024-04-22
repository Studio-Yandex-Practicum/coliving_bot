from internal_requests.entities import ProfileSearchSettings

ASK_SEARCH_SETTINGS = (
    "Будем искать соседа по таким параметрам\n" "или хочешь настроить поиск заново?"
)
SEARCH_INTRO = (
    "Все готово для начала поиска соседа с учетом выбранных настроек."
    " Используй /cancel в любое время, чтобы остановить поиск."
    "\nУдачи!"
)

ASK_LOCATION = "Давай найдем тебе соседа. В каком городе ты планируешь жить?"
ASK_SEX = "С кем планируешь делить жильё?"
ASK_AGE = "Соседа какого возраста хочешь найти?"
PROFILE_LIKE_TEXT = (
    "Отлично! Пользователь {} получил твой лайк, если это окажется взаимно, "
    "тебе придет уведомление."
)
NO_MATCHES = (
    "К сожалению, больше нет подходящих тебе соседей.\n"
    "Ты можешь подождать пока они появятся или изменить критерии для поиска."
)
END_OF_SEARCH = (
    "Надеюсь, ты смог найти себе соседа.\n"
    "А если нет, помни, что ты всегда можешь начать поиск заново."
)
LIKE_NOTIFICATION = "Кто-то хочет стать твоим соседом, посмотрим кто это?"
SEND_LIKE = "<b>Вы только что лайкнули {receiver_name}</b>"
BUTTON_ERROR_MSG = "Выбери соответствующий вариант."


def format_search_settings_message(filters: ProfileSearchSettings) -> str:
    """Формирует сообщение с настройками поиска."""
    result = f"""
    <b>Текущие настройки поиска соседа:</b>

    <b>Город:</b> {filters.location}
    <b>Пол соседа:</b> {filters.sex if filters.sex is not None else "Неважно"}
    """
    if filters.age_max is None:
        result += f"<b>Возраст:</b> >{filters.age_min}"
    else:
        result += f"<b>Возраст:</b> {filters.age_min}-{filters.age_max}"
    return result
