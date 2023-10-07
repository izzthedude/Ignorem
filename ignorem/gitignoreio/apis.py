import json
from typing import Literal, overload

import requests

from ignorem.base.apis import BaseAPI
from ignorem.gitignoreio.models import TemplateModel
from ignorem.gitignoreio.types import TTemplate
from ignorem.gitignoreio.urls import GITIGNORE_API


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
        response = requests.get(GitIgnoreListAPI.url(), params={"format": format_})
        response.raise_for_status()

        if format_ == "lines":
            lines_data: list[str] = json.loads(response.text)
            return lines_data

        elif format_ == "json":
            _data: dict[str, TTemplate] = json.loads(response.text)
            json_data = [
                TemplateModel.from_dict(template) for template in _data.values()
            ]
            return json_data

        raise ValueError("This method only accepts 'lines' or 'json'")


class GitIgnoreAPI(BaseAPI):
    @staticmethod
    def url() -> str:
        return f"{GITIGNORE_API}"

    @staticmethod
    def get(*keys: str) -> str:
        response = requests.get(GitIgnoreAPI.url(), params=keys)
        response.raise_for_status()
        return str(response.text)  # need to appease mypy
