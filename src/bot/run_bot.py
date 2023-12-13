from telegram import Update

from bot import create_bot_app
from error_handler.callback_funcs import error_handler
from utils.logger import configure_logging


def main():
    configure_logging()
    application = create_bot_app()
    application.add_error_handler(error_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
