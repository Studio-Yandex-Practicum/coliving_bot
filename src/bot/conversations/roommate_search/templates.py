from internal_requests.entities import ProfileSearchSettings

PROFILE_DATA = """
<b>Имя:</b> {name}
<b>Пол:</b> {sex}
<b>Возраст:</b> {age}
<b>Город:</b> {location}
<b>О себе:</b> {about}
"""

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
ASK_NEXT_PROFILE = (
    "Отлично! Этот пользователь получил твой лайк, если это окажется взаимно, "
    "тебе придет уведомление.\nХочешь продолжить поиск?"
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
SEND_LIKE = "Вы только что лайкнули {receiver_name}"
BUTTON_ERROR_MSG = "Выбери соответствующий вариант."


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
