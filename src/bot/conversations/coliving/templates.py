from internal_requests.entities import Coliving

LOCATION_FIELD = "location"
ROOM_TYPE_FIELD = "room_type"
ABOUT_FIELD = "about"
PRICE_FIELD = "price"
IS_VISIBLE_FIELD = "is_visible"
ROOMMATES_FIELD = "roommates"
VIEWERS_FIELD = "viewers"
IMAGE_FIELD = "image"

MIN_ABOUT_LENGTH = 0
MAX_ABOUT_LENGTH = 1000
MIN_PRICE = 0
MAX_PRICE = 1000000

DEFAULT_ERROR_MESSAGE = "Некорректный ввод."

IS_VISIBLE_YES = "\nАнкета видна в поиске."
IS_VISIBLE_NO = "\nАнкета скрыта из поиска."

ERR_MSG_ABOUT_MAX_LEN = (
    "Описание не должно содержать более {max} символов. Попробуй ещё раз:"
)
ERR_MSG_PRICE = "Введи цену от {min} до {max}."
ERR_NEED_TO_SELECT_BTN = "Выбери необходимый вариант из меню."
ERR_PHOTO_NOT_TEXT = "Отправь до 5 фотографий своего коливинга."

REPLY_MSG_HELLO = "Привет! Давай проверим твой коливинг:"
REPLY_MSG_TIME_TO_CREATE_PROFILE = (
    "У тебя ещё не создан коливинг! " "\n" "Самое время его создать!"
)
REPLY_MSG_ASK_LOCATION = "Где организован коливинг?"
REPLY_MSG = "Твой ответ:"
REPLY_MSG_WHAT_TO_EDIT = "Что хочешь изменить?"
REPLY_BTN_HIDE = (
    "Твой ответ: Скрыть из поиска"
    "\n"
    "\n"
    "Анкета скрыта из поиска. "
    "Не забудь открыть анкету для поиска позже, "
    "чтобы найти соседей."
)
REPLY_BTN_SHOW = "Твой ответ: Показать в поиске" "\n" "\n" "Анкета доступна для поиска."
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
    "Теперь покажи свой коливинг."
    " Желательно показать кухню, общие зоны, санузел и комнаты,"
    " где будут жить твои соседи. Можно загрузить до 5 фотографий."
)
REPLY_MSG_PHOTO = "Какой классный коливинг получается 🫠. Он выглядит так: "
REPLY_MSG_ASK_TO_CONFIRM = "\nВсё верно?"
REPLY_MSG_TITLE = "Сейчас анкета коливинга выглядит так: \n\n"
REPLY_MSG_ASK_TO_SHOW_PROFILE = (
    "Сделать коливинг доступным для поиска?" "\n" "Этот параметр можно изменить позже."
)
REPLY_MSG_PROFILE_NO_CHANGE = "Что ж, анкета осталась как есть."
REPLY_MSG_START_CREATE_PROFILE = "Для создания профиля введи /coliving."
REPLY_MSG_PROFILE_SAVED = "Отлично! Изменения сохранены."

BTN_EDIT_PROFILE = "edit_profile"
BTN_LABEL_EDIT_PROFILE_KEYBOARD = "Изменить профиль коливинга"
BTN_HIDE = "hide"
BTN_LABEL_HIDE_SEARCH_KEYBOARD = "Скрыть из поиска 🚫"
BTN_SHOW = "show"
BTN_LABEL_SHOW = "Показать в поиске 🔍"
BTN_ROOMMATES = "roommates_profiles"
BTN_LABEL_ROOMMATES = "Посмотреть анкеты соседей"
BTN_VIEWS = "views"
BTN_LABEL_VIEWS = "Просмотры"
BTN_TRANSFER_TO = "transfer_to"
BTN_LABEL_TRANSFER_TO = "Передача коливинга"
BTN_GO_TO_MENU = "go_to_menu"

LOCATION_CALLBACK_DATA = "select_location"

ROOM_TYPE_CALLBACK_DATA = "select_room_type"
BTN_LABEL_BED_IN_ROOM = "Спальное место"
BTN_LABEL_ROOM_IN_APPARTMENT = "Комната"

BTN_CONFIRM = "confirm"
BTN_LABEL_CONFIRM = "Да, подтвердить"
BTN_CANCEL = "cancel"
BTN_LABEL_CANCEL = "Отменить"
BTN_CANCEL_EDIT = "cancel"
BTN_LABEL_CANCEL_EDIT = "Отменить редактирование ❌"
BTN_FILL_AGAIN = "edit_fill_again"
BTN_LABEL_FILL_AGAIN = "Заполнить заново ✏️"
BTN_EDIT_ROOM_TYPE = "edit_room_type"
BTN_LABEL_EDIT_ROOM_TYPE = "Тип аренды"
BTN_EDIT_ABOUT_ROOM = "edit_about"
BTN_LABEL_EDIT_ABOUT_ROOM = "Описание"
BTN_EDIT_PRICE = "edit_price"
BTN_LABEL_EDIT_PRICE = "Цена"
BTN_EDIT_PHOTO = "edit_send_photo"
BTN_LABEL_EDIT_PHOTO = "Фото квартиры"
BTN_EDIT_CONTINUE = "continue_editing"
BTN_LABEL_EDIT_CONTINUE = "Продолжить редактирование"
BTN_INVITE_ROOMMATES = "invite_roommate"
BTN_LABEL_INVITE_ROOMMATES = "Пригласить в коливинг"
BTN_DELETE_ROOMMATES = "delete_roommate"
BTN_LABEL_DELETE_ROOMMATES = "Удалить из коливинга"
BTN_REPORT_ROOMMATES = "report_to"
BTN_LABEL_REPORT_ROOMMATES = "Пожаловаться на пользователя"
BTN_DELETE_CONFIRM = "confirm_delete"
BTN_LABEL_DELETE_CONFIRM = "Да, удалить"
BTN_EDIT_LOCATION = "edit_location"
BTN_LABEL_EDIT_LOCATION = "Местоположение"

PROFILE_DATA = (
    "<b>Город:</b> {location}\n"
    "<b>Тип аренды:</b> {room_type}\n"
    "<b>Описание:</b> {about}\n"
    "<b>Стоимость:</b> {price} р./мес.\n"
)


async def format_coliving_profile_message(coliving_info: Coliving) -> str:
    result = REPLY_MSG_TITLE + PROFILE_DATA.format(
        location=coliving_info.location,
        room_type=coliving_info.room_type,
        about=coliving_info.about,
        price=coliving_info.price,
    )
    if isinstance(coliving_info.is_visible, bool):
        if coliving_info.is_visible:
            result += IS_VISIBLE_YES
        else:
            result += IS_VISIBLE_NO
    return result
