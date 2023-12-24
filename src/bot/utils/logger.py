import logging
from logging import handlers

from utils.configs import (
    LOGGING_LEVEL,
    LOGS_BACKUP_COUNT,
    LOGS_ENCODING,
    LOGS_FILE_PATH,
    LOGS_FOLDER,
    LOGS_FORMAT,
    LOGS_INTERVAL,
    LOGS_WHEN,
)


def configure_logging() -> None:
    """
    Logging configuration for a file and console.
    """
    LOGS_FOLDER.mkdir(parents=True, exist_ok=True)

    console_handler = logging.StreamHandler()
    file_handler = handlers.TimedRotatingFileHandler(
        filename=LOGS_FILE_PATH,
        when=LOGS_WHEN,
        interval=LOGS_INTERVAL,
        backupCount=LOGS_BACKUP_COUNT,
        encoding=LOGS_ENCODING,
    )

    logging.basicConfig(
        level=LOGGING_LEVEL,
        format=LOGS_FORMAT,
        handlers=(
            console_handler,
            file_handler,
        ),
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
