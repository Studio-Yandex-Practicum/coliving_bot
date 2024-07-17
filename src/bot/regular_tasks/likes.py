from telegram.ext import ContextTypes

from internal_requests import api_service


async def delete_old_likes(_context: ContextTypes.DEFAULT_TYPE):
    """Отправляет запрос на удаление лайков"""
    return await api_service.delete_old_likes()
