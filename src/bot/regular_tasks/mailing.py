import asyncio
import logging
from base64 import b64decode

from telegram.error import Forbidden
from telegram.ext import CallbackContext

from internal_requests import api_service

_LOGGER = logging.getLogger(__name__)


async def check_mailing_list(context: CallbackContext):
    """
    Проверка наличия сообщений для рассылки.
    """
    _LOGGER.info("Starting check_mailing_list")
    data = await api_service.get_mailing()
    _LOGGER.debug("Received mailing data: %s", data)

    if data:
        data["page"] = 1
        await api_service.update_mail(data["id"], "is_sending")
        context.job_queue.run_once(
            callback=process_users_for_mailing, when=0, data=data
        )
    else:
        _LOGGER.info("No messages found for mailing")


async def process_users_for_mailing(context: CallbackContext):
    """
    Получает список пользователей для отправки рассылки
    и вызывает соответствующие методы.
    """
    data = context.job.data
    _LOGGER.info("Processing users for mailing, current page: %s", data["page"])
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
        await api_service.update_mail(data["id"], "is_sent")
        _LOGGER.info("Mailing successfully sent for mail ID: %s", data["id"])


async def send_mail_with_image(context: CallbackContext, data: dict, users: list):
    """
    Отправка пользователям из списка сообщений с картинки.
    """
    _LOGGER.info("Sending mail with image to %d users", len(users))

    await _send_first_message_with_image(context, data, users)

    for user in users:
        try:
            await context.bot.send_photo(
                chat_id=user["telegram_id"],
                photo=data["file_id"],
                caption=data["text"],
            )
        except Forbidden as exc:
            _LOGGER.debug(
                f"Failed to send message to user {user["telegram_id"]}: {str(exc)}"
            )
        await asyncio.sleep(1)


async def send_mail_without_image(context: CallbackContext, data: dict, users: list):
    """
    Отправка пользователям из списка сообщений без картинки.
    """
    _LOGGER.info("Sending mail without image to %d users", len(users))
    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user["telegram_id"], text=data["text"]
            )
        except Forbidden as exc:
            _LOGGER.debug(
                f"Failed to send message to user {user['telegram_id']}: {str(exc)}"
            )

        await asyncio.sleep(1)


async def _send_first_message_with_image(
    context: CallbackContext, data: dict, users: list
):
    """
    Отправляет первое сообщение рассылки с изображением.
    Сохраняет file_id изображения в контекст для дальнейшей рассылки.
    """
    if data.get("file_id") is None:
        while users:
            user = users.pop()
            try:
                image = b64decode(data["image"])
                message = await context.bot.send_photo(
                    chat_id=user["telegram_id"],
                    photo=image,
                    caption=data["text"],
                )
                data["file_id"] = message.photo[-1].file_id
                return
            except Forbidden:
                _LOGGER.debug(f"Forbidden exception for {user}. Trying next user.")
                continue
