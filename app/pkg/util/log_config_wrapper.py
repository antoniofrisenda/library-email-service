_LOG_SETUP = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False
        },
        "pymongo": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False
        },
        "boto3": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False
        },
        "botocore": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False
        },
        "urllib3": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG"
    },
}
