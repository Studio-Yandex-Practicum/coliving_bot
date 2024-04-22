from internal_requests.entities import ColivingSearchSettings

COLIVING_DATA = """
<b>Город:</b> {location}
<b>Тип коливинга:</b> {room_type}
<b>Цена:</b> {price}
<b>О коливинге:</b> {about}
"""
ASK_SEARCH_SETTINGS = (
    "Будем искать коливинг по таким параметрам\n" "или хочешь настроить поиск заново?"
)
SEARCH_INTRO = (
    "Все готово для начала поиска коливинга с учетом выбранных настроек."
    " Используй команду /cancel в любое время,"
    " чтобы остановить поиск.\nУдачи!"
)

SEARCH_START = "Давай найдем тебе коливинг."
ASK_LOCATION = "В каком городе ищешь коливинг?"
ASK_ROOM_TYPE = "Какой тип жилья ты ищешь?"
ASK_PRICE = "За какую цену ты ищешь коливинг?"
ASK_MIN_PRICE = "Укажи минимальную сумму:"
ASK_MAX_PRICE = "Укажи максимальную сумму:"

COLIVING_LIKE_MSG = (
    "Отлично! Организатор коливинга получил твой лайк, если это окажется взаимно, "
    "тебе придет уведомление."
)
NO_MATCHES = (
    "К сожалению, больше нет подходящих тебе объявлений :(\n"
    "Ты можешь подождать, пока они появятся или изменить критерии для поиска:"
)
END_OF_SEARCH = (
    "Надеюсь, ты смог найти себе коливинг.\n"
    "А если нет, помни, что ты всегда можешь начать поиск заново."
)
LIKE_NOTIFICATION = "Кому-то понравился твой коливинг! 🎉 Посмотрим?"

ERR_MSG_ABOUT_COST = "Введи число от {min} до {max}:"

BUTTON_ERROR_MSG = "Выбери соответствующий вариант."


def format_search_settings_message(filters: ColivingSearchSettings) -> str:
    """Формирует сообщение с настройками поиска."""
    result = f"""
    <b>Текущие настройки поиска коливинга:</b>

    <b>Город:</b> {filters.location}
    <b>Тип жилья:</b> {filters.room_type}
    <b>Цена от:</b> {filters.min_price} <b> до </b> {filters.max_price}
    """
    return result
