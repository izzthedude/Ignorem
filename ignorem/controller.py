from __future__ import annotations

import logging

from ignorem.constants import Data
from ignorem.gitignoreio.api import GitIgnoreAPI, GitIgnoreListAPI
from ignorem.gitignoreio.models import TemplateModel
from ignorem.utils import files
from ignorem.utils.singleton import Singleton

logger = logging.getLogger(__name__)


class AppController(Singleton):
    def __init__(self) -> None:
        self._templates: list[TemplateModel] = []
        self._selected: list[TemplateModel] = []
        self._template_text: str = ""

    def request_list(self, fetch: bool = False) -> None:
        logger.info("Requesting template list")

        if not Data.CACHE_FILE.exists() or fetch:
            self._fetch_list()

        templates: list[TemplateModel] = [
            TemplateModel.from_data(template)  # type: ignore
            for template in files.read_json(Data.CACHE_FILE)
        ]

        self._clear_template()
        for template in templates:
            self._add_template(template)

    def request_template(self) -> None:
        keys = [template.key for template in self.selected()]
        logger.info(f"Requesting template text with keys: {keys}")
        self.template_text = GitIgnoreAPI.get(*keys)

    def templates(self) -> list[TemplateModel]:
        return self._templates

    def selected(self) -> list[TemplateModel]:
        return self._selected

    def is_selected(self, template: TemplateModel) -> bool:
        return template in self._selected

    def add_selected(self, template: TemplateModel) -> None:
        logger.debug(f"Adding template: {template.key}")
        self._selected.append(template)

    def remove_selected(self, template: TemplateModel) -> None:
        logger.debug(f"Removing template: {template.key}")
        self._selected.remove(template)

    def clear_selected(self) -> None:
        self._selected.clear()

    @property
    def template_text(self) -> str:
        return self._template_text

    @template_text.setter
    def template_text(self, value: str) -> None:
        self._template_text = value

    def _fetch_list(self) -> None:
        logger.debug("Fetching template list")
        templates = [template.to_data() for template in GitIgnoreListAPI.get("json")]
        files.write_json(templates, Data.CACHE_FILE)

    def _add_template(self, template: TemplateModel) -> None:
        self._templates.append(template)

    def _clear_template(self) -> None:
        self._templates.clear()
