import json

from ignorem.base.types import JSONLike, PathLike


def write_json(obj: JSONLike, path: PathLike) -> None:
    with open(path, "w") as file:
        json.dump(obj, file)


def read_json(path: PathLike) -> JSONLike:
    with open(path, "r") as file:
        return json.load(file)  # type: ignore
