import json

from ignorem.utils.typings import JSONLike, PathLike


def write_json(obj: JSONLike, path: PathLike) -> None:
    with open(path, "w") as file:
        json.dump(obj, file)


def read_json(path: PathLike) -> JSONLike:
    with open(path) as file:
        return json.load(file)  # type: ignore
