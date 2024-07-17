from telegram.ext import ContextTypes

from conversations.coliving.keyboards import create_keyboard_of_locations


async def update_location_keyboard(context: ContextTypes.DEFAULT_TYPE):
    """Поддерживает клавиатуру локаций в актуальном состоянии."""
    context.bot_data["location_keyboard"] = await create_keyboard_of_locations()
