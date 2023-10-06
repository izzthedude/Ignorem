from ignorem import gitignore
from ignorem.constants import Data
from ignorem.gitignore import TemplateData
from ignorem.utils import files


class AppController:
    _instance: "AppController" = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = AppController()
        return AppController._instance

    def __init__(self):
        if AppController._instance:
            raise Exception(
                "An instance of this class already exists. "
                "Use 'AppController.instance()' to get it."
            )

        self._templates: list[TemplateData] = []
        self._selected_templates: list[TemplateData] = []

    def fetch_list(self, force_fetch: bool = False) -> list[TemplateData]:
        cache_file = Data.CACHE_FILE
        if not cache_file.exists() or force_fetch:
            files.write_json(
                [template.as_dict() for template in gitignore.list_json()],
                Data.CACHE_FILE,
            )

        self._templates = [
            TemplateData(**template) for template in files.read_json(Data.CACHE_FILE)
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
