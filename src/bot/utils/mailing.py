from base64 import b64decode

from telegram.ext import CallbackContext

from internal_requests import api_service


async def check_mailing_list(context: CallbackContext):
    """
    Проверка наличия сообщений для рассылки.
    """
    data = await api_service.get_mailing()
    if data:
        data["page"] = 1
        await api_service.update_sended_mail(data["id"], "is_sending")
        context.job_queue.run_once(
            callback=process_users_for_mailing, when=0, data=data
        )


async def process_users_for_mailing(context: CallbackContext):
    """
    Получает список пользователей для отправки рассылки
    и вызывает соответствующие методы.
    """
    data = context.job.data
    if not isinstance(data, dict):
        raise TypeError("Expected data to be a dictionary")
    users_response = await api_service.get_users_for_mailing(page=data["page"])
    users: list = users_response["results"]

    if data.get("image") is not None:
        await send_mail_with_image(context, data, users)
    else:
        await send_mail_without_image(context, data, users)

    if users_response["next"] is not None:
        data["page"] += 1
        context.job_queue.run_once(
            callback=process_users_for_mailing, when=60, data=data
        )
    else:
        await api_service.update_sended_mail(data["id"], "is_sent")


async def send_mail_with_image(context: CallbackContext, data: dict, users: list):
    """
    Отправка пользователям из списка сообщений с картинки.
    """
    for user in users:
        if data.get("file_id") is None:
            image = b64decode(data["image"])
            message = await context.bot.send_photo(
                chat_id=user["telegram_id"],
                photo=image,
                caption=data["text"],
                rate_limit_args=1,
            )
            data["file_id"] = message.photo[-1].file_id
        else:
            await context.bot.send_photo(
                chat_id=user["telegram_id"],
                photo=data["file_id"],
                caption=data["text"],
                rate_limit_args=1,
            )


async def send_mail_without_image(context: CallbackContext, data: dict, users: list):
    """
    Отправка пользователям из списка сообщений без картинки.
    """
    for user in users:
        await context.bot.send_message(
            chat_id=user["telegram_id"], text=data["text"], rate_limit_args=1
        )
