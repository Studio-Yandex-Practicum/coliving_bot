from conversations.profile.constants import MAX_AGE, MIN_AGE, PHOTO_MAX_NUMBER

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
ASK_LOCATION = (
    "В каком городе ты ищешь соседа или коливинг?\n"
    "Сейчас доступны только Москва и Санкт-Петербург,"
    " другие города будут доступны позже."
)
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
AGE_ERR_MSG = f"Можно ввести возраст от {MIN_AGE} до {MAX_AGE} лет."
NAME_LENGTH_ERROR_MSG = "Имя не должно быть меньше {min} и больше {max} символов."
DEFAULT_ERROR_MESSAGE = "Некорректный ввод."
NAME_SYMBOL_ERROR_MSG = (
    "Допустима кириллица и латиница, не используйте цифры и спец. символы."
)
BUTTON_ERROR_MSG = "Выбери соответствующий вариант."
ABOUT_MAX_LEN_ERROR_MSG = "Описание не должно содержать более {max} символов."
PHOTO_ERROR_MESSAGE = "Отправь фото."
ERR_PHOTO_NOT_TEXT = f"Отправь до {PHOTO_MAX_NUMBER} фотографий для своего профиля."
SHORT_PROFILE_DATA = (
    "<b>Имя:</b> {name}\n"
    "<b>Пол:</b> {sex}\n"
    "<b>Возраст:</b> {age}\n"
    "<b>Место поиска:</b> {location}\n"
    "<b>О себе:</b> {about}\n"
)
PROFILE_DATA = SHORT_PROFILE_DATA + "<b>Видимость анкеты:</b> {is_visible}\n"

REPLY_MSG_WANT_TO_DELETE = "Ты уверен, что хочешь удалить свою анкету?"
REPLY_MSG_PROFILE_DELETED = "Твоя анкета была удалена."
REPLY_MSG_PROFILE_NO_CHANGE = "Анкета не была изменена."
CANCEL_PROFILE_CREATION = "Создание анкеты отменено."

DELETE_CANCELED = "Удаление отменено."
CANNOT_BE_DELETED = (
    "Вы состоите в коливинге, либо являетесь его организатором!\n"
    "Чтобы удалить анкету, вам нужно открепиться от коливинга,"
    "либо передать его.\n"
    "Это можно сделать во вкладке 'Мой коливинг' 😉."
)
INVALID_NAME_HYPHEN_ONLY_ERROR_MSG = (
    "Имя не может состоять только из дефисов."
    " Пожалуйста, введи корректное имя, используя кириллицу или латиницу."
)
