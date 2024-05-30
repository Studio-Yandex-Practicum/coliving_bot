from conversations.coliving.constants import PHOTO_MAX_NUMBER
from conversations.common_functions.common_templates import (
    PROFILE_IS_HIDDEN_TEXT,
    PROFILE_IS_VISIBLE_TEXT,
)
from internal_requests.entities import Coliving

ERR_MSG_ABOUT_MAX_LEN = "Описание не должно содержать более {max} символов."
ERR_MSG_PRICE = "Введи цену от {min} до {max}."
ERR_NEED_TO_SELECT_BTN = "Выбери необходимый вариант из меню."
ERR_PHOTO_NOT_TEXT = f"Отправь до {PHOTO_MAX_NUMBER} фотографий своего коливинга."
ERR_PHOTO_LIMIT_TEXT = (
    f"Вы отправили более {PHOTO_MAX_NUMBER} фотографий "
    f"сохранены будут только первые {PHOTO_MAX_NUMBER}"
)

DONT_SAVE_COLIVING_WITHOUT_PHOTO = "Нельзя сохранить коливинг без фото."
REPLY_MSG_HELLO = "Привет! Давай проверим твой коливинг:"
REPLY_MSG_TIME_TO_CREATE_PROFILE = (
    "У тебя ещё не создан коливинг! " "\n" "Самое время его создать!"
)
REPLY_MSG_ASK_LOCATION = "Где организован коливинг?"
REPLY_MSG_WHAT_TO_EDIT = "Что хочешь изменить?"
REPLY_BTN_HIDE = (
    "Анкета скрыта из поиска. "
    "Не забудь открыть анкету для поиска позже, "
    "чтобы найти соседей."
)
REPLY_BTN_SHOW = "Анкета доступна для поиска."

REPLY_MSG_ASK_ROOM_TYPE = "Что сдаётся в аренду в твоём коливинге?"
REPLY_MSG_ASK_ABOUT = (
    "Расскажи о своём коливинге. Как называется?"
    " Есть ли общая тема для объединения? (IT, K-pop, вегетарианство и т.д)."
    " Кого ты хочешь видеть в качестве соседа?"
    " В каком районе или рядом с каким метро находится коливинг?"
    " Расскажи об удобствах внутри коливинга."
    " Расскажи о цене, и что входит в эту цену?"
)
REPLY_MSG_ASK_PRICE = "Укажи цену аренды за месяц (в рублях):"
REPLY_MSG_ASK_PHOTO_SEND = (
    f"Теперь покажи свой коливинг."
    f" Желательно показать кухню, общие зоны, санузел и комнаты,"
    f" где будут жить твои соседи. Можно загрузить до {PHOTO_MAX_NUMBER} фотографий."
)
REPLY_MSG_PHOTO = "Какой классный коливинг получается 😊. Он выглядит так: "
REPLY_MSG_PHOTO_RECEIVE = "\nЖелаете сохранить фотографии?"
REPLY_MSG_ASK_TO_CONFIRM = "\nВсё верно?"
REPLY_MSG_TITLE = "Сейчас анкета коливинга выглядит так: \n\n"
REPLY_MSG_ASK_TO_SHOW_PROFILE = (
    "Сделать коливинг доступным для поиска?" "\n" "Этот параметр можно изменить позже."
)
REPLY_MSG_PROFILE_NO_CHANGE = "Что ж, анкета осталась как есть."
REPLY_MSG_START_CREATE_PROFILE = "Для создания профиля введи /coliving."
REPLY_MSG_PROFILE_SAVED = "Отлично! Изменения сохранены."
REPLY_MSG_PROFILE_NO_CREATE = "Создание коливинга отменено."
REPLY_SAVE_PHOTO = "save"
REPLY_MSG_WANT_TO_DELETE = "Ты уверен что хочешь удалить коливинг?"
REPLY_MSG_PROFILE_DELETED = "Твой коливинг был удален."

PROFILE_DATA = (
    "<b>Город:</b> {location}\n"
    "<b>Тип аренды:</b> {room_type}\n"
    "<b>Описание:</b> {about}\n"
    "<b>Стоимость:</b> {price} р./мес.\n"
    "<b>Видимость анкеты:</b> {is_visible}\n"
)

ROOMMATE_DATA = "<b>Имя:</b> {name}\n" "<b>Возраст:</b> {age}\n"

ROOMMATE_PROFILE_DATA = (
    "<b>Имя:</b> {name}\n"
    "<b>Пол:</b> {sex}\n"
    "<b>Возраст:</b> {age}\n"
    "<b>Место поиска:</b> {location}\n"
    "<b>О себе:</b> {about}\n"
)

ASK_NEXT_ROOMMATE = (
    "Отлично! Этот пользователь получил твое приглашение. "
    "Если он согласится, тебе придет уведомление.\n"
    "Продолжим?"
)

NO_ROOMMATES = "К сожалению, больше некого пригласить 😔"

END_OF_ROOMMATE_ASSIGN = (
    "Если захочешь пригласить кого-то ещё, то ты можешь всегда вернуться! 👋"
)

INVITATION_FOR_ROOMMATE = (
    "Тебя приглашают в коливинг. Нажми ✅, чтобы рассмотреть приглашение"
)

ASSIGN_ROOMMATE_START_MSG = (
    "Сейчас буду по очереди показывать пользователей,"
    " которых можно пригласить в коливинг."
)

CANNOT_INVITE = (
    "Извините, данный пользователь состоит в другом коливинге"
    " или является организатором коливинга. Продолжим?"
)


async def format_coliving_profile_message(coliving_info: Coliving) -> str:
    is_visible = (
        PROFILE_IS_VISIBLE_TEXT if coliving_info.is_visible else PROFILE_IS_HIDDEN_TEXT
    )
    return PROFILE_DATA.format(
        location=coliving_info.location,
        room_type=coliving_info.room_type,
        about=coliving_info.about,
        price=coliving_info.price,
        is_visible=is_visible,
    )
