from typing import TypedDict


class TTemplate(TypedDict, total=True):
    key: str
    name: str
    fileName: str
    contents: str
