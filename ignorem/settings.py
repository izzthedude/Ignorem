import logging.config
import os
from pathlib import Path

APP_ID = "@APP_ID@"
APP_NAME = "@APP_NAME@"
APP_VERSION = "@APP_VERSION@"
APP_AUTHOR = "@APP_AUTHOR@"
APP_LICENSE = "@APP_LICENSE@"
APP_WEBSITE = "@APP_WEBSITE@"
APP_ISSUE_URL = "@APP_ISSUE_URL@"

REQUEST_TIMEOUT = 10  # in seconds

CACHE_DIR = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / APP_ID
STATE_DIR = (
    Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state")) / APP_ID
)

CACHE_DIR.mkdir(parents=True, exist_ok=True)
STATE_DIR.mkdir(parents=True, exist_ok=True)

logging.config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s | %(levelname)s | %(name)s]: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "worker": {
                "format": "[%(asctime)s | WORKER]: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "level": "INFO",
                "formatter": "default",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": f"{STATE_DIR / APP_NAME}.log",
                "level": "DEBUG",
                "formatter": "default",
                "maxBytes": 131072,
                "backupCount": 2,
            },
            "file_worker": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": f"{STATE_DIR / APP_NAME}.log",
                "level": "DEBUG",
                "formatter": "worker",
                "maxBytes": 65536,
                "backupCount": 2,
            },
        },
        "loggers": {
            "": {
                "handlers": [
                    "console",
                    "file",
                ],
                "propagate": False,
            },
            "ignorem": {
                "handlers": [
                    "console",
                    "file",
                ],
                "level": "DEBUG",
                "propagate": False,
            },
            "ignorem.utils.worker": {
                "handlers": [
                    "console",
                    "file_worker",
                ],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
)
