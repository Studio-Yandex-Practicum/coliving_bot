import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
# General data folder path
DATA_PATH = BASE_DIR.parent / ".data"

# Telegram BOT token
TOKEN = os.getenv("TOKEN")

# Logs folder path
LOGS_FOLDER = DATA_PATH / "logs"

# Logger parameters
LOGGING_LEVEL = logging.getLevelName(os.getenv("LOGGING_LEVEL"))
LOGS_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOGS_FILE_PATH = LOGS_FOLDER / "bot.log"
LOGS_WHEN = os.getenv("LOGS_WHEN")
LOGS_INTERVAL = int(os.getenv("LOGS_INTERVAL"))
LOGS_BACKUP_COUNT = int(os.getenv("LOGS_BACKUP_COUNT"))
LOGS_ENCODING = os.getenv("LOGS_ENCODING")

# Internal requests to backend
INTERNAL_API_URL = os.getenv("INTERNAL_API_URL", "http://127.0.0.1:8000/api/v1/")
