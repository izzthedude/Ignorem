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
    data = _get_list()
    return [TemplateData(**template) for template in data.values()]


def list_keys() -> list[str]:
    """
    Gets a list of gitignore templates' keys.

    Returns
    -------
    list[str]
        A list of templates' keys.
    """
    data = _get_list()
    return list(data.keys())


def _get_list() -> dict[str, dict]:
    """Requests a gitignore templates list and converts the response to something that
    Python can understand."""
    response = _request_list("json")
    return json.loads(response.text)


def _request_list(list_format: str = "json") -> requests.Response:
    """Gets a list of gitignore templates in the given format. This function is somewhat
    redundant. It's really only here to show that the API allows options when retrieving
    a list. Nonetheless, this module will enforce the use of the JSON format."""
    response = requests.get(f"{API_URL}/list", params={"format": list_format})
    response.raise_for_status()
    return response
