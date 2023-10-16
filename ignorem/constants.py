from pathlib import Path

from ignorem import settings


class Data:
    CACHE_FILE = Path(settings.CACHE_DIR) / "gitignoreio.json"
    LOGS_FILE = Path(settings.STATE_DIR) / "Ignorem.log"
