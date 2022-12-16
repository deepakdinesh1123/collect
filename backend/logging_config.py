LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "[%(levelname)s] %(asctime)s : %(message)s"},
        "error": {
            "format": "[%(levelname)s] %(asctime)s File: %(pathname)s Message: %(msg)s"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "Error": {
            "level": "ERROR",
            "formatter": "error",
            "class": "logging.FileHandler",
            "filename": "errors.log",
        },
    },
}
