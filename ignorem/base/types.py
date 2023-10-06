import os
from typing import Mapping, Sequence

JSONLike = (
    Mapping[str, str | int | bool] | Mapping[str, "JSONLike"] | Sequence["JSONLike"]
)
PathLike = os.PathLike | str
