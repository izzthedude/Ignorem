import json
from typing import TYPE_CHECKING, Literal, overload

import requests

from ignorem.base.apis import BaseAPI
from ignorem.gitignoreio.models import TemplateModel
from ignorem.gitignoreio.urls import GITIGNORE_API
from ignorem.settings import REQUEST_TIMEOUT

if TYPE_CHECKING:
    from ignorem.gitignoreio.types import TTemplate


class GitIgnoreListAPI(BaseAPI):
    @staticmethod
    def url() -> str:
        return f"{GITIGNORE_API}/list"

    @staticmethod
    @overload
    def get(format_: Literal["lines"]) -> list[str]:
        ...

    @staticmethod
    @overload
    def get(format_: Literal["json"]) -> list[TemplateModel]:
        ...

    @staticmethod
    def get(format_: Literal["lines", "json"]) -> list[str] | list[TemplateModel]:
        response = requests.get(
            GitIgnoreListAPI.url(),
            params={"format": format_},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        if format_ == "lines":
            data: list[str] = json.loads(response.text)
            return data

        data_: dict[str, TTemplate] = response.json()
        return [TemplateModel.from_dict(template) for template in data_.values()]


class GitIgnoreAPI(BaseAPI):
    @staticmethod
    def url() -> str:
        return f"{GITIGNORE_API}"

    @staticmethod
    def get(*keys: str) -> str:
        response = requests.get(
            f"{GitIgnoreAPI.url()}/{','.join(keys)}", timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return str(response.text)  # need to appease mypy
