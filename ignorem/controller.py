from pathlib import Path

from ignorem import gitignore, utils
from ignorem.enums import Paths
from ignorem.gitignore import TemplateData


class AppController:
    _instance: "AppController" = None

    @classmethod
    def instance(cls):
        return AppController._instance if AppController._instance else cls()

    def __init__(self):
        if AppController._instance:
            raise Exception(
                "An instance of this class already exists. "
                "Use 'AppController.instance()' to get it."
            )

        self._templates: list[TemplateData] = []
        self._selected_templates: list[TemplateData] = []

    def fetch_list(self, force_fetch: bool = False) -> list[TemplateData]:
        cache_file = Path(Paths.CACHE_FILE).absolute()
        if not cache_file.exists() or force_fetch:
            utils.write_json(
                [template.as_dict() for template in gitignore.list_json()],
                Paths.CACHE_FILE,
            )

        self._templates = [
            TemplateData(**template) for template in utils.read_json(Paths.CACHE_FILE)
        ]
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
