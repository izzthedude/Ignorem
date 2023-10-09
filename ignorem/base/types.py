from __future__ import annotations

import os
from typing import Any, ClassVar, Mapping, Self, Sequence, Type

JSONLike = (
    Mapping[str, str | int | bool]
    | Mapping[str, Any]
    | Mapping[str, Mapping[str, Any]]
    | Sequence[Mapping[str, Any]]
)
PathLike = os.PathLike | str


class SingletonError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Singletons can only be accessed through the instance() class method."
        )


class Singleton:
    _instance: ClassVar[dict[type[Self], Self]] = {}

    def __new__(cls: type[Self], *args: Any, **kwargs: Any) -> Self:
        if cls in cls._instance:
            raise SingletonError
        return super().__new__(cls)

    @classmethod
    def instance(cls: type[Self]) -> Self:
        if cls not in cls._instance:
            cls._instance[cls] = cls()
        return cls._instance[cls]  # type: ignore
