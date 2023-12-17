MIN_AGE = 18
MAX_AGE = 99
MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 30
MAX_ABOUT_LENGTH = 1000
NAME_PATTERN = '^[А-Яа-яA-Za-z\\s]+$'

AGE_FIELD = 'age'
SEX_FIELD = 'sex'
NAME_FIELD = 'name'
LOCATION_FIELD = 'location'
ABOUT_FIELD = 'about'
IMAGE_FIELD = 'image'
IS_VISIBLE_FIELD = 'is_visible'

ASK_AGE = 'Хорошо. Давай познакомимся. Сколько тебе лет?'
ASK_SEX = 'Какой твой пол?'
ASK_NAME = 'Как тебя зовут?'
ASK_LOCATION = 'В каком городе ты бы хотел жить?'
ASK_ABOUT = 'Расскажи о себе. Чем интересуешься, чем занимаешься.'
ASK_PHOTO = 'Теперь отправь фото. Его будут видеть другие пользователи.'
LOOK_AT_FORM_FIRST = (
    'О, классная фотка. Давай взглянем на то, как выглядит твоя анкета:'
)
LOOK_AT_FORM_SECOND = 'Супер. Теперь твоя анкета выглядит так.'
LOOK_AT_FORM_THIRD = (
    'Мне нравится! Давай взглянем на то, как выглядит твоя анкета:'
)
ASK_IS_THAT_RIGHT = 'Всё верно?'
ASK_FORM_VISIBLE = 'Сделать анкету видимой в поиске?'
FORM_SAVED = 'Спасибо, анкета успешно сохранена.'
FORM_EDIT_SAVED = 'Отлично! Изменения сохранены.'
FORM_NOT_CHANGED = 'Хорошо. Анкета не изменилась.'
FORM_IS_VISIBLE = 'Теперь твоя анкета видна в поиске.'
FORM_IS_NOT_VISIBLE = 'Теперь твоя анкета не видна в поиске.'
ASK_WANT_TO_CHANGE = 'Что ты хочешь изменить?'
ASK_AGE_AGAIN = 'Сколько тебе лет?'
ASK_NEW_PHOTO = 'Отправь новое фото.'
# fmt: off
AGE_LENGHT_ERROR_MSG = (
    'Неверный возраст. Должен быть в диапазоне от {min} до {max}. Повторите ввод.'
)
# fmt: on
AGE_TYPE_ERROR_MSG = 'Возраст должен быть указан как целое число.'
# fmt: off
NAME_LENGHT_ERROR_MSG = (
    'Слишком короткое имя. Должно быть в диапазоне от {min} до {max}. Повторите ввод.'
)
# fmt: on
NAME_SYMBOL_ERROR_MSG = (
    'Неверное имя. Не должно содержать спецсимволы. Повторите ввод.'
)
BUTTON_ERROR_MSG = 'Выбери соответствующий вариант.'
ABOUT_MAX_LEN_ERROR_MSG = (
    'Превышено максимальное количество символов равное {max}.'
)
PHOTO_ERROR_MESSAGE = 'Отправь фото.'
PROFILE_DATA = (
    '<b>Имя:</b> {name}\n'
    '<b>Пол:</b> {sex}\n'
    '<b>Возраст:</b> {age}\n'
    '<b>Место проживания:</b> {location}\n'
    '<b>О себе:</b> {about}\n'
    '<b>Видимость анкеты:</b> {is_visible}\n'
)
