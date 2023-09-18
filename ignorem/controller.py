from pathlib import Path

from ignorem import gitignore, utils
from ignorem.enums import Paths
from ignorem.gitignore import TemplateData


class AppController:
    def __init__(self):
        self._templates: list[TemplateData] = []
        self._selected_templates: list[TemplateData] = []

    def fetch_list(self) -> list[TemplateData]:
        cache_file = Path(Paths.CACHE_FILE).absolute()
        if not cache_file.exists():
            utils.write_json(gitignore.list_json(), Paths.CACHE_FILE)

        self._templates = utils.read_json(Paths.CACHE_FILE)
        return self._templates

    def templates(self) -> list[TemplateData]:
        return self._templates

    def selected_templates(self) -> list[TemplateData]:
        return self._selected_templates

    def add_selected_template(self, template: TemplateData):
        self._selected_templates.append(template)

    def remove_selected_template(self, template: TemplateData):
        self._selected_templates.remove(template)

    def request_template(self) -> str:
        keys = [template.key for template in self._selected_templates]
        return gitignore.get_template(keys)

    def reset(self):
        self._selected_templates.clear()
