from abc import abstractmethod
from typing import Any, Protocol


class BaseAPI(Protocol):
    @staticmethod
    @abstractmethod
    def url() -> str:
        raise NotImplementedError

    @staticmethod
    def get(*args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @staticmethod
    def insert(*args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @staticmethod
    def update(*args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @staticmethod
    def delete(*args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
