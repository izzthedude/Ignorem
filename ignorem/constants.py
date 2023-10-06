import os
from pathlib import Path

from ignorem import settings


class Paths:
    CACHE_DIR: str = str(
        Path(os.environ.get("XDG_CACHE_HOME"), settings.APP_ID).absolute()
    )
    CACHE_FILE: str = str(Path(CACHE_DIR, "templates_cache.json"))

    Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)
