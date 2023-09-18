import os
from pathlib import Path


class Ignorem:
    ID = "@APP_ID@"
    NAME = "@APP_NAME@"
    VERSION = "@APP_VERSION@"
    AUTHOR = "@APP_AUTHOR@"
    LICENSE = "@APP_LICENSE@"
    WEBSITE = "@APP_WEBSITE@"
    ISSUE_URL = "@APP_ISSUE_URL@"


class Paths:
    CACHE_DIR: str = str(Path(os.environ.get("XDG_CACHE_DIR"), Ignorem.ID).absolute())
    CACHE_FILE: str = str(Path(CACHE_DIR, "templates_cache.json"))
