import os
from pathlib import Path

from ignorem import settings


class Paths:
    CACHE_DIR: Path = (
        Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / settings.APP_ID
    )
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


class Data:
    CACHE_FILE: Path = Path(Paths.CACHE_DIR, "gitignoreio.json")
