from dataclasses import asdict, dataclass, fields
from typing import Any, Mapping, Self, Sequence

from ignorem.gitignoreio.types import TTemplate


@dataclass
class TemplateModel:
    key: str
    name: str
    fileName: str
    contents: str

    @classmethod
    def fields(cls) -> Sequence[str]:
        return tuple(field.name for field in fields(cls))

    @classmethod
    def from_dict(cls, data: TTemplate) -> Self:
        return cls(**data)

    def to_dict(self) -> TTemplate | Mapping[str, Any]:
        return asdict(self)
