from logging.handlers import TimedRotatingFileHandler

from .base import *  # noqa

log_path = BASE_DIR.parent / ".data/logs"
log_path.mkdir(parents=True, exist_ok=True)
log_filename = log_path / "backend.log"

SITE_URL = "http://158.160.140.97"
ALLOWED_HOSTS += ["158.160.140.97"]
CSRF_TRUSTED_ORIGINS = (SITE_URL,)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "file": {
            "level": os.getenv("LOGGING_LEVEL", "INFO"),
            "class": TimedRotatingFileHandler,
            "filename": log_filename,
            "when": os.getenv("LOGS_WHEN", "midnight"),
            "interval": int(os.getenv("LOGS_INTERVAL", 1)),
            "backupCount": int(os.getenv("LOGS_BACKUP_COUNT", 14)),
            "encoding": os.getenv("LOGS_ENCODING", "utf-8"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
        },
    },
}
