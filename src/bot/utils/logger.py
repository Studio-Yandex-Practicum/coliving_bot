import logging
from logging import handlers

from .config import LOGS_FOLDER

# Logger handlers for console and file
console_handler = logging.StreamHandler()
file_handler = handlers.TimedRotatingFileHandler(
    filename=LOGS_FOLDER / 'logs.txt',
    when='midnight',
    interval=1,
    backupCount=14,
    encoding='utf-8'
)

logger = logging.getLogger('logger')
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logging.getLogger('httpx').setLevel(logging.WARNING)
