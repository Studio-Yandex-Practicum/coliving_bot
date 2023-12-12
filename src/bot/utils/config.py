import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
# General data folder path
DATA_PATH = BASE_DIR.parent / ".data"

TOKEN = os.getenv("TOKEN")

# Logs folder creation/ folder route
LOGS_FOLDER = DATA_PATH / "logs"
LOGS_FOLDER.mkdir(parents=True, exist_ok=True)

# Logger config
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
