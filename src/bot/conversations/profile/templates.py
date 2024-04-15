MIN_AGE = 18
MAX_AGE = 99
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 30
MIN_ABOUT_LENGTH = 0
MAX_ABOUT_LENGTH = 1000
PHOTO_MAX_NUMBER = 3
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

ASK_AGE = "Сколько тебе лет?"
ASK_SEX = "Ты парень или девушка?"
ASK_NAME = (
    "У тебя ещё нет профиля. Давай заполним простую форму,"
    " это очень важно для твоего будущего соседа."
    "\n\nКак тебя зовут? Я Flat White, как кофе, да."
    " Я считаю, будущего соседа всегда можно позвать на чашку кофе,"
    " чтобы хорошо провести время ☺️"
)
ASK_NAME_AGAIN = "Как тебя зовут?"
ASK_LOCATION = "В каком городе ты ищешь соседа или коливинг?"
ASK_ABOUT = (
    "Расскажи о себе немного: чем ты занимаешься?"
    " Кем работаешь? На кого учишься?"
    " Чем увлекаешься? Какую музыку слушаешь?"
    " Что ожидаешь от соседа и места проживания?"
)
ASK_PHOTO = (
    "Не секрет, что первое впечатление - это очень важно! Найди свои лучшие фотографии"
    " и загрузи их, затем нажми кнопку 'Сохранить фото' 😉"
    "\np.s. загрузить можно не более 3 фотографий."
)
PHOTO_ADDED = "Классные фото! Сохранил! 📸"
DONT_SAVE_WITHOUT_PHOTO = "Сохранить анкету без фото нельзя."
LOOK_AT_FORM_FIRST = "Вау! Фото класс! Давай посмотрим, что получилось 🤩"
LOOK_AT_FORM_SECOND = "Супер. Теперь твоя анкета выглядит так:"
LOOK_AT_FORM_THIRD = "Давай посмотрим, что получилось 😊:"
ASK_IS_THAT_RIGHT = "Всё верно?"
ASK_FORM_VISIBLE = (
    "Отлично, твоя анкета сейчас открыта и видна всем. Оставляем анкету видимой?"
)
FORM_SAVED = "Отлично, анкета сохранена."
FORM_EDIT_SAVED = "Отлично! Изменения сохранены."
FORM_NOT_CHANGED = "Что ж, анкета осталась как есть."
PROFILE_VIEWING = "Это твоя анкета. Что хочешь сделать?"
ASK_WANT_TO_CHANGE = "Хорошо. Давай исправим 🤔"
# fmt: off
AGE_ERROR_MSG = "Введи целое число от {min} до {max}:"
NAME_LENGHT_ERROR_MSG = "Введи имя от {min} до {max} символов:"
# fmt: on
DEFAULT_ERROR_MESSAGE = "Некорректный ввод."
NAME_SYMBOL_ERROR_MSG = "Введи имя без цифр и спецсимволов:"
BUTTON_ERROR_MSG = "Выбери соответствующий вариант."
ABOUT_MAX_LEN_ERROR_MSG = (
    "Описание не должно содержать более {max} символов. Попробуй еще раз:"
)
PHOTO_ERROR_MESSAGE = "Отправь фото."
ERR_PHOTO_NOT_TEXT = f"Отправь до {PHOTO_MAX_NUMBER} фотографий для своего профиля."
PROFILE_DATA = (
    "<b>Имя:</b> {name}\n"
    "<b>Пол:</b> {sex}\n"
    "<b>Возраст:</b> {age}\n"
    "<b>Место поиска:</b> {location}\n"
    "<b>О себе:</b> {about}\n"
    "<b>Видимость анкеты:</b> {is_visible}\n"
)
