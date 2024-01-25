import os
from typing import Iterable, Mapping

JSONLike = (
    Mapping[str, str | int | bool] | Mapping[str, "JSONLike"] | Iterable["JSONLike"]
)
PathLike = os.PathLike[str] | str
