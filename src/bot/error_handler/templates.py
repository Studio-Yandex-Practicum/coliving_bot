# Шаблон сообщения для пользователя Telegram.
ERROR_MESSAGE_TEMPLATE = """
Запрос был совершен с ошибкой, возможно, были указаны неправильные данные.

Возможно проблема на стороне сервера, обязательно свяжитесь с поддержкой!

<b>Ошибка: {error}</b>
"""
# Шаблон для логов
LOGGING_MESSAGE_TEMPLATE = """
"Exception while handling an update:"
f"\ncontext.user_data={user_data}"
f"\ncontext.chat_data={chat_data}"
"""
