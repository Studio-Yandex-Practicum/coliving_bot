from .base import * # noqa


LOGGING_SETTINGS = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "file": {
            "level":  os.getenv("LOGGING_LEVEL"),
            "class": TimedRotatingFileHandler,
            "filename": BASE_DIR.parent / ".data/logs/django.log",
            "when": os.getenv("LOGS_WHEN"),
            "interval": int(os.getenv("LOGS_INTERVAL")),
            "backupCount": int(os.getenv("LOGS_BACKUP_COUNT")),
            "encoding": os.getenv("LOGS_ENCODING"),
            "formatter": "verbose",
        },
        "console": {
            "level": os.getenv("LOGGING_LEVEL"),
            "class": "logging.StreamHandler",
            "formatter": "verbose",
         },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
        },
    }
}
