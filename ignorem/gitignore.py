from dataclasses import dataclass, asdict, astuple
import json
import requests


API_URL = "https://www.toptal.com/developers/gitignore/api"


@dataclass
class TemplateData:
    """
    The TemplateData class represents a gitignore template data in JSON format when
    a list of templates is requested as JSON.
    """

    fileName: str
    name: str
    contents: str
    key: str

    def as_dict(self):
        return asdict(self)

    def as_tuple(self):
        return astuple(self)


def get_template(keys: list[str]) -> str:
    """
    Gets a gitignore template with the given keys.

    Parameters
    ----------
    keys : list[str]
        A list of gitignore template keys.

    Returns
    -------
    str
        A gitignore template.
    """
    response = requests.get(f"{API_URL}/{','.join(keys)}")
    return response.text


def list_json() -> list[TemplateData]:
    """
    Gets a list of gitignore templates in JSON format.

    Returns
    -------
    list[TemplateData]
        A list of TemplateData objects.
    """
    response = _list("json")
    data: dict[str, dict] = json.loads(response.content)
    result = [TemplateData(**template) for key, template in data.items()]
    return result


def list_keys() -> list[str]:
    """
    Gets a list of gitignore templates keys.

    Returns
    -------
    list[str]
        A list of template keys.
    """
    response = _list("lines")
    result = response.text.split("\n")
    return result


def _list(format_: str) -> requests.Response:
    """
    Gets a list of gitignore templates in the given format.

    Parameters
    ----------
    format_ : str
        The format of the templates list.
        Possible values: 'lines' and 'json'

    Returns
    -------
    requests.Response
        A Response object of the requested templates list.
    """
    response = requests.get(f"{API_URL}/list", params={"format": format_})
    response.raise_for_status()
    return response
