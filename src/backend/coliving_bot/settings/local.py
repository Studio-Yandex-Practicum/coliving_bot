from .base import *  # noqa

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "level": "INFO",
            "handlers": [
                "console",
            ],
        },
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
    },
}
