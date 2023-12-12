from telegram import Update

from bot import create_bot_app


def main():
    application = create_bot_app()
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
