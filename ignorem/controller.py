from __future__ import annotations

from ignorem.base.types import Singleton
from ignorem.constants import Data
from ignorem.gitignoreio.apis import GitIgnoreAPI, GitIgnoreListAPI
from ignorem.gitignoreio.models import TemplateModel
from ignorem.utils import files


class AppController(Singleton):
    def __init__(self) -> None:
        self._templates: list[TemplateModel] = []
        self._selected_templates: list[TemplateModel] = []

    def fetch_list(self, force_fetch: bool = False) -> list[TemplateModel]:
        cache_file = Data.CACHE_FILE
        if not cache_file.exists() or force_fetch:
            files.write_json(
                [template.to_dict() for template in GitIgnoreListAPI.get("json")],
                Data.CACHE_FILE,
            )

        self._templates = [
            TemplateModel(**template) for template in files.read_json(Data.CACHE_FILE)
        ]
        return self._templates

    def templates(self) -> list[TemplateModel]:
        return self._templates

    def selected_templates(self) -> list[TemplateModel]:
        return self._selected_templates

    def add_selected_template(self, template: TemplateModel) -> None:
        self._selected_templates.append(template)

    def remove_selected_template(self, template: TemplateModel) -> None:
        self._selected_templates.remove(template)

    def request_template(self) -> str:
        keys = [template.key for template in self._selected_templates]
        return GitIgnoreAPI.get(*keys)

    def reset(self) -> None:
        self._selected_templates.clear()
