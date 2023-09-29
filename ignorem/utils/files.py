import json


def write_json(obj, path: str):
    with open(path, "w") as file:
        json.dump(obj, file)


def read_json(path: str):
    with open(path, "r") as file:
        return json.load(file)
