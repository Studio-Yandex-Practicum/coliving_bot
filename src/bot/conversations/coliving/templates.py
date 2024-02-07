from internal_requests.entities import Coliving

COLIVING_START = "coliving"
COLIVING_START_BTN = "Коливинг"

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

DEFAULT_ERROR_MESSAGE = "Некорректный ввод"

IS_VISIBLE_YES = "\nАнкета видна в поиске"
IS_VISIBLE_NO = "\nАнкета скрыта из поиска"

ERR_MSG_ABOUT_MAX_LEN = "Превышено максимальное количество символов равное {max}."
ERR_MSG_PRICE = "Цена, должна быть целым числом от {min} до {max}. Повторите ввод!"
ERR_NEED_TO_SELECT_BTN = "Пожалуйста, выберите вариант из предложенных."
ERR_PHOTO_NOT_TEXT = "Пожалуйста, отправьте 5 фотографий"

REPLY_MSG_HELLO = "Привет! давай проверим твой коливинг"
REPLY_MSG_TIME_TO_CREATE_PROFILE = (
    "У вас еще не создан коливинг! " "\n" "Самое время его создать! "
)
REPLY_MSG_ASK_LOCATION = "Где организован коливинг?"
REPLY_MSG = "Ваш ответ: "
REPLY_MSG_WHAT_TO_EDIT = "Что хотите изменить?"
REPLY_BTN_HIDE = (
    "Ваш ответ: Скрыть из поиска"
    "\n"
    "\n"
    "Анкета скрыта из поиска. "
    "Не забудьте установить этот параметр позже, "
    "чтобы найти соседей."
)
REPLY_BTN_SHOW = "Ваш ответ: Показать в поиске" "\n" "\n" "Анкета доступна для поиска."
REPLY_MSG_ASK_ROOM_TYPE = "Выберите тип помещения:"
REPLY_MSG_ASK_ABOUT = (
    "Расскажи о своей квартире." "\n" "Краткое описание коливинга и его жильцов ?"
)
REPLY_MSG_ASK_PRICE = "Укажите цену аренды за месяц?"
REPLY_MSG_ASK_PHOTO_SEND = (
    "Теперь можете отправить фото, квартиры. "
    "\n"
    "Пожалуйста, загрузите до 5 фотографий"
)
REPLY_MSG_PHOTO = (
    "О, классная квартира. " "\n" "Давай взглянем на то, как выглядит твой коливинг:"
)
REPLY_MSG_ASK_TO_CONFIRM = "\nВсё верно?"
REPLY_MSG_TITLE = "Твой коливинг: \n\n"
REPLY_MSG_ASK_TO_SHOW_PROFILE = (
    "Сделать профиль доступным для поиска? "
    "\n"
    "Этот параметр можно установить позже."
)
REPLY_MSG_PROFILE_NO_CHANGE = "Хорошо, анкета не изменилась."
REPLY_MSG_START_CREATE_PROFILE = "Для создания профиля введите /coliving."
REPLY_MSG_PROFILE_SAVED = "Профиль успешно сохранен!"

BTN_EDIT_PROFILE = "edit_profile"
BTN_LABEL_EDIT_PROFILE_KEYBOARD = "Изменить коливинг профиль"
BTN_HIDE = "hide"
BTN_LABEL_HIDE_SEARCH_KEYBOARD = "Скрыть из поиска"
BTN_SHOW = "show"
BTN_LABEL_SHOW = "Показать в поиске"
BTN_ROOMMATES = "roommates_profiles"
BTN_LABEL_ROOMMATES = "Посмотреть анкеты соседей"
BTN_VIEWS = "views"
BTN_LABEL_VIEWS = "Просмотры"
BTN_TRANSFER_TO = "transfer_to"
BTN_LABEL_TRANSFER_TO = "Передача коливинга"
BTN_GO_TO_MENU = "go_to_menu"
BTN_LABEL_GO_TO_MENU = "Вернуться в меню"

LOCATION_CALLBACK_DATA = "select_location"

ROOM_TYPE_CALLBACK_DATA = "select_room_type"
BTN_LABEL_BED_IN_ROOM = "Спальное место"
BTN_LABEL_ROOM_IN_APPARTMENT = "Комната"

BTN_CONFIRM = "confirm"
BTN_LABEL_CONFIRM = "Да, подтвердить"
BTN_CANCEL = "cancel"
BTN_LABEL_CANCEL = "Отменить"
BTN_CANCEL_EDIT = "cancel"
BTN_LABEL_CANCEL_EDIT = "Отменить редактирование"
BTN_FILL_AGAIN = "edit_fill_again"
BTN_LABEL_FILL_AGAIN = "Заполнить заново"
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
    "<b>Место проживания:</b> {location}\n"
    "<b>Тип аренды:</b> {room_type}\n"
    "<b>Описание:</b> {about}\n"
    "<b>Цена:</b> {price} р/мес\n"
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
