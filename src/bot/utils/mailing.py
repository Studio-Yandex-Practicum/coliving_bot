from base64 import b64decode
from datetime import datetime

from telegram.ext import ContextTypes

from internal_requests import api_service


async def send_mailing_list(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Функция для рассылок.
    """
    mail = await api_service.get_mailing()
    send_date = datetime.strptime(mail["send_date"], "%Y-%m-%dT%H:%M:%SZ")

    if send_date <= datetime.now() and mail["is_sended"] is False:
        page = 1
        while True:
            try:
                users_response = await api_service.get_users_for_mailing(page=page)
                users = users_response["results"]
            except KeyError:
                break

            for user in users:
                if mail["image"]:
                    image = b64decode(mail["image"])
                    await context.bot.send_photo(
                        chat_id=user["telegram_id"], photo=image, caption=mail["text"]
                    )
                else:
                    await context.bot.send_message(
                        chat_id=["telegram_id"],
                        text=mail["text"],
                    )
            page += 1
        await api_service.update_sended_mail(mail["id"])
