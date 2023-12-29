from __future__ import annotations

import json
import posixpath
from typing import Literal, overload

import requests

from ignorem.constants import URL
from ignorem.gitignoreio.models import TemplateModel
from ignorem.settings import REQUEST_TIMEOUT


class GitIgnoreListAPI:
    @staticmethod
    def url() -> str:
        return posixpath.join(URL.GITIGNORE_API, "list")

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

        return [
            TemplateModel.from_data(template) for template in response.json().values()
        ]


class GitIgnoreAPI:
    @staticmethod
    def url() -> str:
        return URL.GITIGNORE_API

    @staticmethod
    def get(*keys: str) -> str:
        response = requests.get(
            f"{GitIgnoreAPI.url()}/{','.join(keys)}", timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.text
