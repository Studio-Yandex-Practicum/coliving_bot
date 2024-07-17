import logging

from telegram.ext import ContextTypes

from internal_requests import api_service

_LOGGER = logging.getLogger(__name__)


async def update_useful_materials_for_relevance(
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Обновляет в контексте список полезных материалов для поддержки актуальности."""
    context.bot_data["useful_info"] = await api_service.get_useful_materials()
    _LOGGER.info("Полезные материалы обновлены.")
