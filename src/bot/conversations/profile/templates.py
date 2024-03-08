from conversations.profile.buttons import HIDE_SEARCH_BUTTON, SHOW_SEARCH_BUTTON

MIN_AGE = 18
MAX_AGE = 99
MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 30
MIN_ABOUT_LENGTH = 0
MAX_ABOUT_LENGTH = 1000
NAME_PATTERN = "^[А-Яа-яA-Za-z'-]+$"
AGE_PATTERN = "^([0-9]{3})$"

AGE_FIELD = "age"
SEX_FIELD = "sex"
NAME_FIELD = "name"
LOCATION_FIELD = "location"
ABOUT_FIELD = "about"
IMAGE_FIELD = "image"
IS_VISIBLE_FIELD = "is_visible"
RECEIVED_PHOTOS_FIELD = "received_photos"

ASK_AGE = (
    "Давай познакомимся поближе, это очень важно для твоего будущего соседа."
    " А сколько тебе лет? "
)
ASK_SEX = "А ты парень или девушка?"
ASK_NAME = (
    "А как тебя зовут? Я Flat White, как кофе, да."
    " Я считаю, будущего соседа всегда можно позвать на чашку кофе,"
    " чтобы хорошо провести время ☺️"
)
ASK_LOCATION = "В каком городе ты ищешь соседа или коливинг?"
ASK_ABOUT = (
    "Расскажи о себе немного: чем ты занимаешься?"
    " Кем ты работаешь? На кого ты учишься?"
    " Чем ты увлекаешься? Какую музыку ты слушаешь?"
    " Что ты ожидаешь от соседа и места проживания?"
)
ASK_PHOTO = (
    "Не секрет, что первое впечатление - это очень важно! Найди свои лучшие фотографии"
    ' и загрузи их, затем нажми "Сохранить" 😉'
)
DONT_SAVE_WITHOUT_PHOTO = "Нельзя сохранить анкету без фото."
LOOK_AT_FORM_FIRST = "Вау! Фото потрясающие! Давай посмотрим, что получилось 🤩"
LOOK_AT_FORM_SECOND = "Супер. Теперь твоя анкета выглядит так."
LOOK_AT_FORM_THIRD = "Давай посмотрим что получилось 😊:"
ASK_IS_THAT_RIGHT = "Всё верно?"
ASK_FORM_VISIBLE = "Начнём поиск? Оставляем анкету видимой?"
FORM_SAVED = "Я сохранил изменения анкеты."
FORM_EDIT_SAVED = "Отлично! Изменения сохранены."
FORM_NOT_CHANGED = "Что ж, анкета осталась как есть."
FORM_IS_VISIBLE = (
    f"<b>Твой ответ:</b> {SHOW_SEARCH_BUTTON}\nТеперь твоя анкета видна в поиске."
)
FORM_IS_NOT_VISIBLE = (
    f"<b>Твой ответ:</b> {HIDE_SEARCH_BUTTON}\nТеперь твоя анкета не видна в поиске."
)
ASK_WANT_TO_CHANGE = "Хорошо. Давай это исправим 🤔"
ASK_AGE_AGAIN = "А сколько тебе лет?"
# fmt: off
AGE_ERROR_MSG = (
    'Неверный возраст. Должен быть целым числом от {min} до {max}. Повторите ввод.'
)
NAME_LENGHT_ERROR_MSG = (
    'Слишком короткое имя. Должно быть от {min} до {max}. Повторите ввод.'
)
# fmt: on
DEFAULT_ERROR_MESSAGE = "Некорректный ввод"
NAME_SYMBOL_ERROR_MSG = (
    "Неверное имя. Не должно содержать цифры и спецсимволы. Повторите ввод."
)
BUTTON_ERROR_MSG = "Выбери соответствующий вариант."
ABOUT_MAX_LEN_ERROR_MSG = "Превышено максимальное количество символов равное {max}."
PHOTO_ERROR_MESSAGE = "Отправь фото."
PROFILE_DATA = (
    "<b>Имя:</b> {name}\n"
    "<b>Пол:</b> {sex}\n"
    "<b>Возраст:</b> {age}\n"
    "<b>Место проживания:</b> {location}\n"
    "<b>О себе:</b> {about}\n"
    "<b>Видимость анкеты:</b> {is_visible}\n"
)
PROFILE_IS_VISIBLE_TEXT = "Отображается в поиске"
PROFILE_IS_INVISIBLE_TEXT = "Скрыта из поиска"
