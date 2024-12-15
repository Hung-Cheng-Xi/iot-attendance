import logging


def configure_logging():
    logging_config = {
        "version": 1,
        "formatters": {
            "simpleFormatter": {
                "format": (
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "uvicornFormatter": {
                "class": "uvicorn.logging.ColourizedFormatter",
                "format": "%(levelprefix)s %(asctime)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "consoleHandler": {
                "class": "logging.StreamHandler",
                "formatter": "uvicornFormatter",
                "level": "DEBUG",
            },
            "fileHandler": {
                "class": "logging.FileHandler",
                "formatter": "simpleFormatter",
                "filename": "app.log",
                "mode": "a",
                "level": "DEBUG",
            },
        },
        "loggers": {
            "": {
                "level": "DEBUG",
                "handlers": ["consoleHandler", "fileHandler"],
            },
            "uvicorn": {
                "level": "DEBUG",
                "handlers": ["consoleHandler", "fileHandler"],
                "propagate": False,
            },
            "uvicorn.error": {
                "level": "DEBUG",
                "handlers": ["consoleHandler", "fileHandler"],
                "propagate": True,
            },
            "uvicorn.access": {
                "level": "DEBUG",
                "handlers": ["consoleHandler", "fileHandler"],
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(logging_config)
