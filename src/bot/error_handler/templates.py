# Шаблон сообщения для пользователя Telegram.
ERROR_MESSAGE_TEMPLATE = """
Ой, что-то пошло не так. Попробуйте позже.
"""
# Шаблон для логов
LOGGING_MESSAGE_TEMPLATE = """
"Exception while handling an update:"
f"\ncontext.user_data={user_data}"
f"\ncontext.chat_data={chat_data}"
"""
