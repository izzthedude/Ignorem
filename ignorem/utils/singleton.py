from __future__ import annotations

from typing import Any, ClassVar, Self


class SingletonError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Singletons can only be accessed through the instance() class method."
        )


class Singleton:
    _instances: ClassVar[dict[type[Self], Self]] = {}

    def __new__(cls: type[Self], *args: Any, **kwargs: Any) -> Self:
        if cls in cls._instances:
            raise SingletonError
        return super().__new__(cls)

    @classmethod
    def instance(cls: type[Self]) -> Self:
        if cls not in cls._instances:
            cls._instances[cls] = cls()
        return cls._instances[cls]  # type: ignore
