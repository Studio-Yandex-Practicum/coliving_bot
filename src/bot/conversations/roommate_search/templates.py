from conversations.profile.constants import MAX_AGE, MIN_AGE
from conversations.roommate_search.buttons import ANY_AGE_BTN, ANY_GENDER_BTN
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
ASK_AGE_MIN = "Какой минимальный возраст ты бы предпочёл у своего соседа?"
ASK_AGE_MAX = (
    "Отлично! А какой максимальный возраст ты бы хотел видеть у своего соседа?"
)
AGE_ERR_MSG = f"Можно ввести возраст от {MIN_AGE} до {MAX_AGE} лет."
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
    <b>Пол соседа:</b> {ANY_GENDER_BTN if filters.sex is None else filters.sex}
    <b>Возраст:</b> {_get_age_range_string_from_search_settings(filters)}"""
    return result


def _get_age_range_string_from_search_settings(filters: ProfileSearchSettings) -> str:
    """Возвращает текстовое представление для диапазона возраста желаемого соседа."""
    age_min, age_max = filters.age_min, filters.age_max
    if age_min or age_max:
        return f"от {age_min} " * bool(age_min) + f"до {age_max}" * bool(age_max)
    return ANY_AGE_BTN
