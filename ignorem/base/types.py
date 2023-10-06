from __future__ import annotations

import os
from typing import Any, Mapping, Self, Sequence, Type

JSONLike = (
    Mapping[str, str | int | bool] | Mapping[str, "JSONLike"] | Sequence["JSONLike"]
)
PathLike = os.PathLike | str


class SingletonError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Singletons can only be accessed through the instance() class method."
        )


class Singleton:
    _instance: dict[Type[Self], Self] = {}

    def __new__(cls: Type[Self], *args: Any, **kwargs: Any) -> Self:
        if cls in cls._instance:
            raise SingletonError
        return super().__new__(cls)

    @classmethod
    def instance(cls: Type[Self]) -> Self | Singleton:
        if cls not in cls._instance:
            cls._instance[cls] = cls()
        return cls._instance[cls]
